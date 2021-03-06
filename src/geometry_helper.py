#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the GeometryHelper class.
"""

import numpy

from src.robot_error import ErrorCode, RobotError
from src.debug import Debug

import json

import os
try:
    import configparser
except:
    from six.moves import configparser


class GeometryHelper:
    """
    This class offers some transformations and helper functions between the uArm frame and an simplified user frame.
    """
    def __init__(self):
        """
        Constructor, defines basic values of user frame.
        :param edge_length: side length of unit cube in mm
        :type edge_length: floats
        :param x_offset: offset of user frame in x direction in mm
        :type x_offset: float
        :param y_offset: offset of user frame in y direction in mm
        :type y_offset: float
        :param z_offset: offset of user frame in z direction in mm
        :type z_offset: float
        :param xy_base_offset: offset of workspace in xy-plane
        :type xy_base_offset: float
        :param z_base_offset: offset of uarm base in z-direction in mm
        :type z_base_offset: float
        :param min_radius_xy: minimum workspace radius
        :type min_radius_xy:float
        :param max_radius_xy: maximum workspace radius
        :type max_radius_xy: float
        """

        self.load_general_options()
    
    def load_general_options(self):
        parent_path = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
        path = os.path.join(parent_path,"config/config.ini")
        parser = configparser.ConfigParser()
        parser.read(path)
        
        self.__edge_length = json.loads(parser['ROBOT']['edge_length'])
        self.__x_offset = json.loads(parser['ROBOT']['x_offset'])
        self.__y_offset = json.loads(parser['ROBOT']['y_offset'])
        self.__z_offset = json.loads(parser['ROBOT']['z_offset'])
        self.__xy_base_offset = json.loads(parser['ROBOT']['xy_base_offset'])
        self.__z_base_offset = json.loads(parser['ROBOT']['z_base_offset'] )
        self.__min_radius_xy = json.loads(parser['ROBOT']['min_radius_xy'])
        self.__max_radius_xy = json.loads(parser['ROBOT']['max_radius_xy'])
        self.__servo_three_limits= json.loads(parser['ROBOT']['servo_three_limit'])


    def transform_position_user_to_uarm(self, x_user, y_user, z_uarm):
        """
        Transform x, y -position in user frame to x, y position in uarm frame. For user frame specification refer
        to the board design.
        :param x_user: x-position in user frame
        :type x_user: int
        :param y_user: y-position in user frame
        :type y_user: int
        :param z_uarm: z-position in uarm frame
        :type z_uarm: float
        :return: position in uarm frame {'x': x, 'y', y}
        :rtype: dict
        """
        # transform coordinates
        # adding .5 to be in center of square
        x_uarm = (x_user + .5) * self.__edge_length + self.__x_offset
        y_uarm = (y_user + .5) * self.__edge_length + self.__y_offset

        # check if input is in range of robot
        # TODO (ALR): This is just a basic workspace restriction, add more if necessary.
        xy_length = numpy.sqrt(x_uarm ** 2 + y_uarm ** 2)
        xy_radius = abs(xy_length - self.__xy_base_offset)
        z_radius = abs(z_uarm - self.__z_base_offset)
        radius = numpy.sqrt(xy_radius ** 2 + z_radius ** 2)
        if radius > (self.__max_radius_xy - self.__xy_base_offset) or x_uarm < 0 or xy_length <= self.__min_radius_xy:
            message = "Die eingegebenen Koordinaten sind nicht f??r den Roboter erreichbar."
            raise RobotError(ErrorCode.E0000, message)

        return {'x': x_uarm, 'y': y_uarm}

    def calculate_equal_wrist_rotation_new(self, x_uarm_old, x_uarm_new, y_uarm_old, y_uarm_new, wrist_old):
        """
        Calculates new wrist rotation that keeps the gripper rotation equal in the world frame. 
        Since we adjust the gripper before turning the pump on to maximize the possible angle, this will be adjusted as well to a new version
        :param x_uarm_old: old x-position in uarm frame
        :type x_uarm_old: float
        :param x_uarm_new: new x-position in uarm frame
        :type x_uarm_new: float
        :param y_uarm_old: old y-position in uarm frame
        :type y_uarm_old: float
        :param y_uarm_new: new y-position in uarm frame
        :type y_uarm_new: float
        :param wrist_old: old wrist position in degrees (absolute servo angle)
        :type wrist_old: float
        :return: new wrist angle that keeps the object in the same orientation
        :rtype: float
        """
        # angle from world x-axis to arm
        alpha_1_rad = numpy.arctan2(y_uarm_old, x_uarm_old)
        alpha_2_rad = numpy.arctan2(y_uarm_new, x_uarm_new)
        alpha_1_deg = numpy.degrees(alpha_1_rad)
        alpha_2_deg = numpy.degrees(alpha_2_rad)
        # calculate degree difference 
        
        beta_1 =  alpha_2_deg -alpha_1_deg
        
        # Calculates the best possible rotation
        final_rot = self.gripper_angle_rotation(wrist_old,beta_1)
        return final_rot
    
    def gripper_angle_rotation(self,current_angle,angle_rotation):
        """
        @Param: Returns the possible result, if one
        current_angle: float, degree: Current angle of the gripper
        angle_rotation: float, degree: The gripper should be rotated by this amount
        @goal: aims to be as far away of 90 degree as possible to allow additional 90 degree turns
        """
        angle_rotation %= 180
        
        rot = [angle_rotation,angle_rotation -180]

        
        # Possible rotation for the same result (given 180 grad rot. symmetry)
        result = []
        for i in rot:
            result.append(i + current_angle)


        
        # Checks, if a result is possible. Else, do the best possible solution
        final_angle =self.__servo_three_limits[0]
        for i in result:
            if i > self.__servo_three_limits[0] and i < self.__servo_three_limits[1]:
                return i
        print("Could not do the desired rotation due to the servo limitations. Therefore, the closest possible rotation is done")
        final_angle = self.__servo_three_limits[0]  # initialize angle with a random but reasonable value
        loss = 360 # tries to minimize loss and uses a high value in the initialization
        for angle in result:
            for limit in self.__servo_three_limits:
                tmp = numpy.absolute(angle - limit)
                if tmp < loss:
                    final_angle = limit
                    loss = tmp
        return final_angle
        
        
   
        
        
    
    def calculate_equal_wrist_rotation(self, x_uarm_old, x_uarm_new, y_uarm_old, y_uarm_new, wrist_old):
        """
        Calculates new wrist rotation that keeps the gripper rotation equal in the world frame.
        :param x_uarm_old: old x-position in uarm frame
        :type x_uarm_old: float
        :param x_uarm_new: new x-position in uarm frame
        :type x_uarm_new: float
        :param y_uarm_old: old y-position in uarm frame
        :type y_uarm_old: float
        :param y_uarm_new: new y-position in uarm frame
        :type y_uarm_new: float
        :param wrist_old: old wrist position in degrees (absolute servo angle)
        :type wrist_old: float
        :return: new wrist angle that keeps the object in the same orientation
        :rtype: float
        """
        # angle from world x-axis to arm
        alpha_1_rad = numpy.arctan2(y_uarm_old, x_uarm_old)
        alpha_2_rad = numpy.arctan2(y_uarm_new, x_uarm_new)
        alpha_1_deg = numpy.degrees(alpha_1_rad)
        alpha_2_deg = numpy.degrees(alpha_2_rad)
        # angle from world x-axis to end effector orientation (-90 because of the asymetric servo range 0-180)
        beta_1 = alpha_1_deg + 90.0 - wrist_old
        # calculate the corresponding new wrist angle for new position, so that the orientation of the grabbed object
        # stays the same
        wrist_new = -beta_1 + alpha_2_deg + 90.0
        # check that the wrist angle is within the servos range
        if not (0 <= wrist_new <= 180):
            message = "Bei der gew??nschten Bewegung kann die orientierung des Objekts nicht beibehalten werden," \
                      "bitte drehen Sie das Object vor der Bewegung."
            raise RobotError(ErrorCode.E0003, message)

        return wrist_new
    
    def adjust_wrist_rotation_before_pumpe_an(self, x_user, y_user):
        """
        Adjust the wrist rotation before picking up a block. Since we have only a max possible wrist angle range of 156 degree ( 12-168 degree), we need to use every degree carefully.
        :param x_uarm: x-position in uarm frame
        :type X_uarm: float
        :param y_uarm: old y-position in uarm frame
        :type y_uarm: float
        :return: new wrist angle that keeps the object in the same orientation
        :rtype: float
        """
        # angle from world x-axis to arm but without the need of a block center position since we only need the angle!
        x_uarm_2 = (x_user ) * self.__edge_length + self.__x_offset
        y_uarm_2 = (y_user ) * self.__edge_length + self.__y_offset
        alpha_1_rad = numpy.arctan2(y_uarm_2, x_uarm_2)
        alpha_1_deg = numpy.degrees(alpha_1_rad)
        # Note: angle on (0,0) point of board 180 Grad, angle on (0,15) => 0 Grad
        
        # The rotation needs to be reversed
        if alpha_1_deg < (self.__servo_three_limits[0]-90):
            mot_angle = self.__servo_three_limits[0]
        elif alpha_1_deg > (self.__servo_three_limits[1]-90):
            mot_angle = self.__servo_three_limits[1]
        else:
            
            mot_angle = alpha_1_deg + 90  
        
        return mot_angle

    def transform_height_user_to_uarm(self, z_user, x_uarm, y_uarm):
        """
        Transform z-position in user frame to uarm frame, check if values are valid.
        :param z_user: z-position in user frame
        :type z_user: int
        :param x_uarm: x-position in uarm frame
        :type x_uarm: float
        :param y_uarm: y-position in uarm frame
        :type y_uarm: float
        :return: z position in uarm frame in mm
        :rtype: float
        """
        # calculate height in uarm frame
        z_uarm = self.__z_offset + z_user * self.__edge_length

        # check if height is valid
        xy_length = numpy.sqrt(x_uarm**2 + y_uarm**2)
        xy_radius = abs(xy_length - self.__xy_base_offset)
        z_radius = abs(z_uarm - self.__z_base_offset)
        radius = numpy.sqrt(xy_radius**2 + z_radius**2)
        # check if z_uarm value in workspace
        if radius > (self.__max_radius_xy - self.__xy_base_offset) or z_uarm < self.__z_offset or z_uarm < self.__edge_length + self.__z_offset:
            message = "Die gew??nschte H??he ist f??r den Roboter nicht erreichbar, bitte geben Sie einen anderen Wert an."
            raise RobotError(ErrorCode.E0004, message)

        return z_uarm



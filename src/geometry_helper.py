#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the GeometryHelper class.
"""

import numpy

from src.robot_error import ErrorCode, RobotError


class GeometryHelper:
    """
    This class offers some transformations and helper functions between the uArm frame and an simplified user frame.
    """
    def __init__(self, edge_length=40, x_offset=0, y_offset=-320, z_offset=10, min_radius=120, max_radius=346):
        """
        Constructor, defines basic values of user frame.
        :param edge_length: side length of unit cube in mm
        :type edge_length: float
        :param x_offset: offset of user frame in x direction in mm
        :type x_offset: float
        :param y_offset: offset of user frame in y direction in mm
        :type y_offset: float
        :param z_offset: offset of user frame in z direction in mm
        :type z_offset: float
        :param min_radius: minimum workspace radius
        :type min_radius:float
        :param max_radius: maximum workspace radius
        :type max_radius: float
        """
        self.__edge_length = edge_length
        self.__x_offset = x_offset
        self.__y_offset = y_offset
        self.__z_offset = z_offset
        self.__min_radius = min_radius
        self.__max_radius = max_radius

    def transform_position_user_to_uarm(self, x_user, y_user):
        """
        Transform x, y position in user frame to x, y position in uarm frame. For user frame specification refer 
        to the board design.
        :param x_user: x position in user frame
        :type x_user: int
        :param y_user: y position in user frame
        :type y_user: int
        :return: position in uarm frame {'x': x, 'y', y}
        :rtype: dict
        """
        # transform coordinates
        # adding .5 to be in center of square
        x_uarm = (x_user + .5) * self.__edge_length + self.__x_offset
        y_uarm = (y_user + .5) * self.__edge_length + self.__y_offset

        # check if input is in range of robot
        xy_radius = numpy.sqrt(x_uarm**2 + y_uarm**2)
        if x_uarm < 0 or not (self.__min_radius <= xy_radius <= self.__max_radius):
            message = "Die eingegebenen Koordinaten sind nicht für den Roboter erreichbar."
            raise RobotError(ErrorCode.E0000, message)

        # TODO: ADD GRIPPER ROTATION

        return {'x': x_uarm, 'y': y_uarm}

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
        alpha_1 = numpy.arctan2(y_uarm_old, x_uarm_old)
        alpha_2 = numpy.arctan2(y_uarm_new, x_uarm_new)
        # angle from world x-axis to end effector orientation (-90 because of the asymetric servo range 0-180)
        beta_1 = alpha_1 - 90.0 + wrist_old
        # calculate the corresponding new wrist angle for new position, so that the orientation of the grabbed object
        # stays the same
        wrist_new = beta_1 - alpha_2 + 90.0
        # check that the wrist angle is within the servos range
        if not (0 <= wrist_new <= 180):
            message = "Bei der gewünschten Bewegung kann die orientierung des Objekts nicht beibehalten werden," \
                      "bitte drehen Sie das Object vor der Bewegung."
            raise RobotError(ErrorCode.E0003, message)

        return wrist_new

    def transform_height_user_to_uarm(self, z_user):
        """
        Transform z-position in user frame to uarm frame, check if values are valid.
        :param z_user: z position in user frame
        :type z_user: int
        :return: z position in uarm frame in mm
        :rtype: float
        """
        



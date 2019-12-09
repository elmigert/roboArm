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
    def __init__(self, edge_length=40, x_offset=0, y_offset=-320, z_offset=10, xy_base_offset=174, z_base_offset=93.5, min_radius_xy=120, max_radius_xy=340):
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
        :param xy_base_offset: offset of workspace in xy-plane
        :type xy_base_offset: float
        :param z_base_offset: offset of uarm base in z-direction in mm
        :type z_base_offset: float
        :param min_radius_xy: minimum workspace radius
        :type min_radius_xy:float
        :param max_radius_xy: maximum workspace radius
        :type max_radius_xy: float
        """
        self.__edge_length = edge_length
        self.__x_offset = x_offset
        self.__y_offset = y_offset
        self.__z_offset = z_offset
        self.__xy_base_offset = xy_base_offset
        self.__z_base_offset = z_base_offset
        self.__min_radius_xy = min_radius_xy
        self.__max_radius_xy = max_radius_xy

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
        # TODO: This is not at all accurate, check if this is good enough.
        xy_length = numpy.sqrt(x_uarm ** 2 + y_uarm ** 2)
        xy_radius = abs(xy_length - self.__xy_base_offset)
        z_radius = abs(z_uarm - self.__z_base_offset)
        radius = numpy.sqrt(xy_radius ** 2 + z_radius ** 2)
        if radius > (self.__max_radius_xy - self.__xy_base_offset) or x_uarm < 0 or xy_length <= self.__min_radius_xy:
            message = "Die eingegebenen Koordinaten sind nicht für den Roboter erreichbar."
            raise RobotError(ErrorCode.E0000, message)

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
        alpha_1_rad = numpy.arctan2(y_uarm_old, x_uarm_old)
        alpha_2_rad = numpy.arctan2(y_uarm_new, x_uarm_new)
        alpha_1_deg = numpy.degrees(alpha_1_rad)
        alpha_2_deg = numpy.degrees(alpha_2_rad)
        # angle from world x-axis to end effector orientation (-90 because of the asymetric servo range 0-180)
        beta_1 = alpha_1_deg - 90.0 + wrist_old
        # calculate the corresponding new wrist angle for new position, so that the orientation of the grabbed object
        # stays the same
        wrist_new = beta_1 - alpha_2_deg + 90.0
        # check that the wrist angle is within the servos range
        if not (0 <= wrist_new <= 180):
            message = "Bei der gewünschten Bewegung kann die orientierung des Objekts nicht beibehalten werden," \
                      "bitte drehen Sie das Object vor der Bewegung."
            raise RobotError(ErrorCode.E0003, message)

        return wrist_new

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
        if radius > (self.__max_radius_xy - self.__xy_base_offset) or z_uarm < self.__z_offset:
            message = "Die gewünschte Höhe ist für den Roboter nicht erreichbar, bitte geben Sie einen niedrigeren Wert an."
            raise RobotError(ErrorCode.E0004, message)

        return z_uarm



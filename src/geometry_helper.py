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
    def __init__(self, edge_length=40, x_offset=0, y_offset=-320, min_radius=120, max_radius=346):
        """
        Constructor, defines basic values of user frame.
        :param edge_length: side length of unit cube in mm
        :type edge_length: float
        :param x_offset: offset of user frame in x direction in mm
        :type x_offset: float
        :param y_offset: offset of user frame in y direction in mm
        :type y_offset: float
        :param min_radius: minimum workspace radius
        :type min_radius:float
        :param max_radius: maximum workspace radius
        :type max_radius: float
        """
        self.__edge_length = edge_length
        self.__x_offset = x_offset
        self.__y_offset = y_offset
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

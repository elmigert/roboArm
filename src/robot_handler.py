#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotHandler class, which handles the communication with the uArm Swift pro.
"""

import time

from src.geometry_helper import GeometryHelper
from src.robot_error import ErrorCode, RobotError
from uarm_python_sdk.uarm.wrapper import SwiftAPI


class RobotHandler:
    def __init__(self):
        """
        Connect on initialization.
        """
        # connect to uArm
        self.__swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        self.__swift.waiting_ready(timeout=5)
        # set general mode: 0
        self.__swift.set_mode(0)
        # reset arm to home
        self.__swift.reset(wait=True, speed=10000)
        # initialize geometry helper
        self.__geometry_helper = GeometryHelper()

        # get pose values in uarm frame
        pose = self.__swift.get_position()
        # check if successful
        if isinstance(pose, list):
            self.__x_uarm = pose[0]
            self.__y_uarm = pose[1]
            self.__z_uarm = pose[2]
        else:
            message = "Die Roboter Position konnte nicht gelesen werden, überprüfe die Verbindung."
            raise RobotError(ErrorCode.E0001, message)

        # get servo value in degrees
        wrist_angle = self.__swift.get_servo_angle(servo_id=3)
        if wrist_angle is not None:
            self.__wrist_angle = wrist_angle
        else:
            message = "Die Servomotor Position konnte nicht gelesen werden, überprüfe die Verbindung."
            raise RobotError(ErrorCode.E0002, message)

    def disconnect(self):
        """
        Disconnect robot.
        """
        self.__swift.flush_cmd()
        time.sleep(3)
        self.__swift.disconnect()

    def position_new(self, x_user, y_user):
        """
        Move robot arm to new position x, y in user frame.
        :param x_user: new x position in user frame.
        :type x_user: int
        :param y_user: new y position in user frame.
        :type y_user: int
        """
        # transform frames of positions
        uarm_dict = self.__geometry_helper.transform_position_user_to_uarm(x_user, y_user)
        x_uarm_new = uarm_dict['x']
        y_uarm_new = uarm_dict['y']

        # calculate new wrist angle that keeps object in the same orientation
        wrist_angle_new = self.__geometry_helper.calculate_equal_wrist_rotation(self.__x_uarm, x_uarm_new,
                                                                                self.__y_uarm, y_uarm_new,
                                                                                self.__wrist_angle)

        # move arm
        self.__swift.set_position(x=x_uarm_new, y=y_uarm_new)
        self.__swift.set_servo_angle(servo_id=3, angle=wrist_angle_new)
        self.__swift.flush_cmd()

        # set new values
        self.__x_uarm = x_uarm_new
        self.__y_uarm = y_uarm_new
        self.__wrist_angle = wrist_angle_new

    def hight_new(self, z_user):
        """
        Move robot arm to z position in user frame.
        :param z_user: new height in user frame
        :type z_user: int
        """


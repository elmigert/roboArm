#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotHandler class, which handles the communication with the uArm Swift pro.
"""

import time

from src.geometry_helper import GeometryHelper
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
        # move arm
        self.__swift.set_position(uarm_dict['x'], uarm_dict['y'])
        self.__swift.flush_cmd()

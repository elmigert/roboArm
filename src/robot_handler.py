#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotHandler class, which handles the communication with the uArm Swift pro.
"""

import time
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

    def disconnect(self):
        """
        disconnect robot
        """
        self.__swift.flush_cmd()
        time.sleep(3)
        self.__swift.disconnect()

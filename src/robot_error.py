#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotError class.
"""

from enum import Enum


class RobotError(Exception):
    """
    Specific error for robot arm project, messages are in german.
    """
    def __init__(self, error_code, message):
        """
        Constructor for robot arm error.
        :param error_code: unique error code
        :type error_code: ErrorCode
        :param message: message of error in german
        :type message: str
        """
        self.__error_code = error_code
        self.__message = message

    @property
    def error_code(self):
        return self.__error_code

    @property
    def message(self):
        return self.__message


class ErrorCode(Enum):
    E0000 = 0   # GeometryHelper
    E0001 = 1   # RobotHandler
    E0002 = 2   # RobotHandler
    E0003 = 3   # GeometryHelper

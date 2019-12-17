#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotError class.
"""

from enum import Enum


class RobotError(Exception):
    """
    Specific error for robot arm project, messages are in german and can be displayed in user interface.
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
    """
    Unique ErrorCOde enum for each error.
    """
    E0000 = 0   # GeometryHelper
    E0001 = 1   # RobotHandler
    E0002 = 2
    E0003 = 3   # GeometryHelper
    E0004 = 4   # GeometryHelper
    E0005 = 5   # RobotHandler
    E0006 = 6   # UserScript
    E0007 = 7   # UserScript
    E0008 = 8   # UserScript
    E0009 = 9   # UserScript
    E0010 = 10  # UserScript
    E0011 = 11  # UserScript

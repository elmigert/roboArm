#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserScript class test.
"""

import unittest

from src.robot_error import RobotError, ErrorCode
from src.user_script import UserScript


class TestUserScript(unittest.TestCase):
    """
    UserScript class unit test.
    """
    def test_init(self):
        """
        Test initialization.
        """
        test_input_string = "position_neu(1, 2)   \nhoehe_neu(2) \n  \n \n \n"
        user_script_1 = UserScript(test_input_string)

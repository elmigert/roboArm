#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserScript class test.
"""

import unittest

from src.robot_error import RobotError, ErrorCode
from src.user_script import UserScript


class MockRobotHandler:
    """
    Mock robot handler class.
    """
    def __init__(self):
        pass

    def position_new(self, position):
        pass

    def height_new(self, height_list):
        pass

    def pump_on(self):
        pass

    def pump_off(self):
        pass

    def reset(self):
        pass


class TestUserScript(unittest.TestCase):
    """
    UserScript class unit test.
    """
    def test_init(self):
        """
        Test initialization.
        """
        test_input_string = "position_neu(1, 2)   \nhoehe_neu(2) \n  \n \n \n"
        mock_robot = MockRobotHandler()
        user_script_1 = UserScript(test_input_string, mock_robot)
        self.assertEqual(user_script_1._UserScript__function_calls[0]["function"], mock_robot.position_new)
        self.assertEqual(user_script_1._UserScript__function_calls[1]["function"], mock_robot.height_new)
        self.assertListEqual(user_script_1._UserScript__function_calls[0]["args"], [1, 2])
        self.assertListEqual(user_script_1._UserScript__function_calls[1]["args"], [2])

    def test_run_reset(self):
        """
        Test running functions defined in input string
        """
        test_input_string = "position_neu(1, 2)   \nhoehe_neu(2) \n  \n \n \n pumpe_an() \n  pumpe_aus()"
        mock_robot = MockRobotHandler()

        user_script_1 = UserScript(test_input_string, mock_robot)
        user_script_1.run_script(mock_robot)
        user_script_1.reset(mock_robot)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the MockRobotHandler class, which mocks the RobotHandler class.
"""

class MockRobotHandler:
    """
    MockRobotHandler class.
    """
    def __init__(self):
        """
        Mock __init__.
        """
        print("Initializing MockRobotHandler.")

    def disconnect(self):
        """
        Mock disconnect method.
        """
        print("Disconnecting MockRobotHandler.")

    def reset(self):
        """
        Mock reset method.
        """
        print("Reset MockRobotHandler.")

    def position_new(self, position_user):
        """
        Mock position_new method.
        """
        print("position_new: ", position_user)

    def height_new(self, z_user_list):
        """
        Mock height_new method.
        """
        print("height_new: ", z_user_list)

    def pump_on(self):
        """
        Mock pump_on method.
        """
        print("pump_on")

    def pump_off(self):
        """
        Mock pump_off method.
        """
        print("pump_off")


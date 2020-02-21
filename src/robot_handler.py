#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotHandler class, which handles the communication with the uArm Swift pro.
"""

import time

from uarm_python_sdk.uarm.wrapper import SwiftAPI

from src.direction_kind import DirectionKind
from src.geometry_helper import GeometryHelper
from src.robot_error import ErrorCode, RobotError


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

        # initialize geometry helper
        self.__geometry_helper = GeometryHelper()

        # initialize empty position values
        self.__x_uarm = 0
        self.__y_uarm = 0
        self.__z_uarm = 0
        self.__wrist_angle = 0
        # set values
        self.reset()

        # set sleep time to wait for servo to finish
        self.__sleep_time = 1.0

    def disconnect(self):
        """
        Disconnect robot.
        """
        self.__swift.flush_cmd()
        time.sleep(3)
        self.__swift.disconnect()

    def reset(self):
        """
        Reset robot, go back to start position.
        """
        # reset arm to home
        self.__swift.reset(wait=True, speed=10000)
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

        # set servo value in degrees
        wrist_angle = 90.0
        self.__swift.set_servo_angle(servo_id=3, angle=wrist_angle)
        self.__wrist_angle = wrist_angle

        self.__swift.flush_cmd()

    def position_new(self, position_user):
        """
        Move robot arm to new position x, y in user frame.
        :param position_user: position in user frame [x_user, y_user]
        :type position_user: list[int]
        """
        [x_user, y_user] = position_user
        # transform frames of positions
        uarm_dict = self.__geometry_helper.transform_position_user_to_uarm(x_user, y_user, self.__z_uarm)
        x_uarm_new = uarm_dict['x']
        y_uarm_new = uarm_dict['y']

        # calculate new wrist angle that keeps object in the same orientation
        wrist_angle_new = self.__geometry_helper.calculate_equal_wrist_rotation(self.__x_uarm, x_uarm_new,
                                                                                self.__y_uarm, y_uarm_new,
                                                                                self.__wrist_angle)

        # move arm
        self.__swift.set_position(x=x_uarm_new, y=y_uarm_new)
        self.__swift.set_wrist(angle=wrist_angle_new, wait=True)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

        # set new values
        self.__x_uarm = x_uarm_new
        self.__y_uarm = y_uarm_new
        self.__wrist_angle = wrist_angle_new

    def height_new(self, z_user_list):
        """
        Move robot arm to z position in user frame.
        :param z_user_list: new height in user frame [z_user]
        :type z_user_list: list[int]
        """
        z_user = z_user_list[0]
        # calculate new height in uarm frame
        z_uarm_new = self.__geometry_helper.transform_height_user_to_uarm(z_user, self.__x_uarm, self.__y_uarm)

        # move arm
        self.__swift.set_position(z=z_uarm_new)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

        # set values
        self.__z_uarm = z_uarm_new

    # DEPRECATED
    def rotate_gripper(self, direction):
        """
        Rotate gripper either 90° left or right, depending on direction.
        :param direction: either left or right
        :type direction: DirectionKind
        """
        if direction is DirectionKind.Left:
            wrist_angle_new = self.__wrist_angle - 90.0
        elif direction is DirectionKind.Right:
            wrist_angle_new = self.__wrist_angle + 90.0
        else:
            raise NotImplementedError()

        if not (0 <= wrist_angle_new <= 180):
            message = "Der Greiffer kann nicht weiter in die gewünschte Richtung gedreht werden."
            raise RobotError(ErrorCode.E0005, message)

        # move robot
        self.__swift.set_wrist(angle=wrist_angle_new, wait=True)
        self.__swift.flush_cmd()
        # time.sleep(self.__sleep_time)

        # set value
        self.__wrist_angle = wrist_angle_new

    # DEPRECATED
    def set_wrist(self, angle):
        self.__swift.set_wrist(angle=angle, wait=True)
        self.__swift.flush_cmd()

    def pump_on(self):
        """
        Turn on the pump.
        """
        self.__swift.set_pump(on=True)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

    def pump_off(self):
        """
        Turn off the pump.
        """
        self.__swift.set_pump(on=False)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

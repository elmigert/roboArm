#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserChallenge class, which is used to monitor the success of a challenge.
"""

from enum import Enum

from src.robot_error import ErrorCode, RobotError


class ChallengeKind(Enum):
    """
    Enum class to distinguish the challenge kinds.
    """
    Beginner = "Anfänger"
    Advanced = 1
    Pro = 3
    StartPosition = 4
    EndPosition = 5


class BlockKind(Enum):
    """
    Enum class to distinguish block kinds.
    """
    One = 1
    Three = 2


class UserChallenge:
    """
    This class monitors user challenge success.
    """
    def __init__(self, challenge, start_coordinates):
        """
        Class initialization.
        :param challenge: Kind of challenge to be monitored.
        :type challenge: ChallengeKind, str
        :param start_coordinates: start position and height of robot in user frame [x, y, z]
        :type start_coordinates: list
        """
        # hard-coded start and end positions of blocks
        self.__all_challenges = {ChallengeKind.Beginner: {ChallengeKind.StartPosition: {BlockKind.One: [[0, 0, 1], [2, 2, 1], [0, 15, 1], [2, 13, 1]],
                                                                                        BlockKind.Three: [[6, 6, 1]]},
                                                          ChallengeKind.EndPosition: {BlockKind.One: [[4, 6, 1], [4, 7, 1], [4, 9, 1], [4, 10, 1]],
                                                                                      BlockKind.Three: [[4, 8, 2]]}
                                                          }}
        self.__challenge = challenge
        # check if challenge is not challenge kind
        if type(challenge) is not ChallengeKind:
            if challenge == ChallengeKind.Beginner.value:
                self.__challenge = ChallengeKind.Beginner
            else:
                message = "Die ausgewählte Schwierigkeitsstufe wurde noch nicht implementiert, bitte wählen Sie eine " \
                          "andere aus."
                raise RobotError(ErrorCode.E0012, message)

        self.__coordinates = start_coordinates
        self.__pump = False

    def record_robot(self, robot, function, args):
        """
        Record movements of robot and positions of blocks.
        :param robot: handler of robot
        :type robot: RobotHandler
        :param function: bound function to robot handler object
        :type function: method
        :param args: arguments of function
        :type args: list
        """
        # check type of function and change members accordingly
        if function == robot.position_new:
            self.__coordinates[0] = args[0]
            self.__coordinates[1] = args[1]
        elif function == robot.height_new:
            self.__coordinates[2] = args[2]
        elif function == robot.pump_on:
            self.__pump = True
        elif function == robot.pump_off:
            self.__pump = False
        else:
            raise NotImplementedError()

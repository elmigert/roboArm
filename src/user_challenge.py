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
    Null = 0
    One = 1
    Three = 2  # assume direction of 1x3x1 block only in y direction


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
        # TODO (ALR): Add objects for blocks.
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
                self.__challenge = self.__all_challenges[ChallengeKind.Beginner]
            else:
                message = "Die ausgewählte Schwierigkeitsstufe wurde noch nicht implementiert, bitte wählen Sie eine " \
                          "andere aus."
                raise RobotError(ErrorCode.E0012, message)

        self.__coordinates = start_coordinates
        self.__block = BlockKind.Null

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
            self.__coordinates[2] = args[0]
        elif function == robot.pump_on:
            # we can change the coordinates in start challenge here, since it is reinitialized every time a script is
            # run
            if self.__coordinates in self.__challenge[ChallengeKind.StartPosition][BlockKind.One]:
                self.__challenge[ChallengeKind.StartPosition][BlockKind.One].remove(self.__coordinates)
                self.__block = BlockKind.One
            elif self.__coordinates in self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]:
                self.__challenge[ChallengeKind.StartPosition][BlockKind.Three].remove(self.__coordinates)
                self.__block = BlockKind.Three
            else:
                message = "Die Pumpe kann nur aktiviert werden, um einen Block aufzuheben."
                raise RobotError(ErrorCode.E0013, message)
        elif function == robot.pump_off:
            # calculate coordinates below gripper
            coordinates = self.__coordinates.copy()
            coordinates[2] -= 1
            # check if a block is held, and there is either ground or another block below
            # TODO (ALR): We don't check if the block is dropped from the air here, might need to add check.
            if self.__block is BlockKind.One:
                self.__challenge[ChallengeKind.StartPosition][BlockKind.One].append(self.__coordinates.copy())
            elif self.__block is BlockKind.Three:
                self.__challenge[ChallengeKind.StartPosition][BlockKind.Three].append(self.__coordinates.copy())
            else:
                message = "Die Pumpe kann nur deaktiviert werden, um einen Block auf das Feld oder einen anderen Block" \
                          "abzulegen."
                raise RobotError(ErrorCode.E0014, message)
            self.__block = BlockKind.Null
        else:
            raise NotImplementedError()

    def success(self):
        """
        Check if the challenge was successful by comparing the current and end positions of the blocks.
        This function would be a lot nicer if objects were used for blocks/positions...
        :return: True if end and current position of all blocks is equal
        :rtype: bool
        """
        current_set_b1 = set()
        current_set_b3 = set()
        end_set_b1 = set()
        end_set_b3 = set()

        # change nested lists to sets of tuples to easily compare them
        [current_set_b1.add(tuple(element)) for element in self.__challenge[ChallengeKind.StartPosition][BlockKind.One]]
        [current_set_b3.add(tuple(element)) for element in self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]]
        [end_set_b1.add(tuple(element)) for element in self.__challenge[ChallengeKind.EndPosition][BlockKind.One]]
        [end_set_b3.add(tuple(element)) for element in self.__challenge[ChallengeKind.EndPosition][BlockKind.Three]]

        d_1 = current_set_b1 - end_set_b1
        d_3 = current_set_b3 - end_set_b3

        if len(d_1) == 0 and len(d_3) == 0:
            return True
        return False

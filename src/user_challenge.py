#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserChallenge class, which is used to monitor the success of a challenge.
"""

from enum import Enum

from src.robot_error import ErrorCode, RobotError
from src.debug import Debug


class ChallengeKind(Enum):
    """
    Enum class to distinguish the challenge kinds.
    """
    
    BridgeOne = "Brücke 1"
    BridgeTwo = "Brücke 2"
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
        # TODO (ALR): Add objects for blocks, this will work for now. (TE) : Probably use text file to load different Exercises?
        # hard-coded start and end positions of blocks
        self.__all_challenges = {ChallengeKind.Beginner: {ChallengeKind.StartPosition: {BlockKind.One: [[3, 4, 1], [5, 5, 1], [2, 12, 1], [5, 11, 1]],
                                                                                        BlockKind.Three: [[6, 6, 1]]},
                                                          ChallengeKind.EndPosition: {BlockKind.One: [[4, 6, 1], [4, 7, 1], [4, 9, 1], [4, 10, 1]],
                                                                                      BlockKind.Three: [[4, 8, 2]]}
                                                          },
                                                          ChallengeKind.BridgeOne: {ChallengeKind.StartPosition: {BlockKind.One: [[4, 3, 1], [7, 6, 1], [2, 12, 1], [5, 11, 1]],
                                                                        BlockKind.Three: [[6, 6, 1],[3,1,1]]},
                                                          ChallengeKind.EndPosition: {BlockKind.One: [[5, 6, 1], [5, 6, 2], [5, 8, 1], [5, 8, 2]],
                                                                                      BlockKind.Three: [[5, 7, 3],[3,1,1]]}
                                                          },
                                                          ChallengeKind.BridgeTwo: {ChallengeKind.StartPosition: {BlockKind.One: [[5, 6, 1], [5, 8, 1], [5, 6, 2], [5, 8, 2]],
                                                                        BlockKind.Three: [[5, 7, 3],[3,1,1],[6,6,1]]},
                                                          ChallengeKind.EndPosition: {BlockKind.One: [[5, 6, 1], [5, 8, 1], [5, 5, 1], [5, 3, 1]],
                                                                                      BlockKind.Three: [[5, 7, 2],[5,4,2]]}
                                                          }
                                                          }
        self.__challenge = challenge
        # check if challenge is not challenge kind
        
        #All challenges which are already implemented
        impl_challenges = [ ChallengeKind.Beginner.value,ChallengeKind.BridgeOne.value,ChallengeKind.BridgeTwo.value] 
        if challenge in impl_challenges:
            for item in ChallengeKind:
                if item.value == challenge:
                    self.__challenge = self.__all_challenges[item] 
                    print('Challenge %s ist gestartet. Viel Erfolg beim Lösen.' %{challenge})              
        else:
            message = "Die Aufgabe  %s ist noch nicht implementiert.  Bitte wählen Sie eine   \
                      andere aus."%{challenge}
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
            Debug.msg('Der Block wird auf der Koordinate {} abgelegt'.format(coordinates[:]))
            #Block coordinate below placed block
            coordinates[2] -= 1
  
            # check if a block is held, and there is either ground or another block below
            valid_pos = False
            if coordinates[2] == 0:
               Debug.msg("Block wurde auf den Boden gelegt")
               valid_pos = True
            elif coordinates in self.__challenge[ChallengeKind.StartPosition][BlockKind.One]:
               Debug.msg("Block wurde auf einen kleinen Block gelegt")
               valid_pos = True
            else:
                for i in range(-1,2,1):
                    # Note: Only one rotation is implemented yet as Three type block has the same rotation in all challenges
                    if [coordinates[0],coordinates[1]+i,coordinates[2]] in self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]:
                            Debug.msg("Block wurde auf einen grossen Block gelegt")
                            valid_pos = True
            if valid_pos:
                if self.__block is BlockKind.One:
                    self.__challenge[ChallengeKind.StartPosition][BlockKind.One].append(self.__coordinates.copy())
                elif self.__block is BlockKind.Three:
                    self.__challenge[ChallengeKind.StartPosition][BlockKind.Three].append(self.__coordinates.copy())
                else:
                    message = "Der Robotor trägt momentan keinen oder keinen bekannten Block"
                    raise RobotError(ErrorCode.E0014, message)
                self.__block = BlockKind.Null
                Debug.msg('Blocks auf Koordinaten: Klein ({}): {} \
                      , Gross  ({}): {} '.format(len(self.__challenge[ChallengeKind.StartPosition][BlockKind.One]),self.__challenge[ChallengeKind.StartPosition][BlockKind.One][:],
                      len(self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]),self.__challenge[ChallengeKind.StartPosition][BlockKind.Three][:]))
            else:
                message = "Der Block kann nicht in der Luft losgelassen werden."
                Debug.error(message)
                raise RobotError(ErrorCode.E0015, message)
                    
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

        #Only check whether the required end position are reached (new version : TE)
        final_positions_one = self.__challenge[ChallengeKind.EndPosition][BlockKind.One]
        final_positions_three = self.__challenge[ChallengeKind.EndPosition][BlockKind.Three]
        for position in self.__challenge[ChallengeKind.StartPosition][BlockKind.One]:      
             is_final = False
             if position in final_positions_one:
                 final_positions_one.remove(position)
                 is_final = True
             Debug.msg("Position {} is in endposition: {}"
                       .format(position,is_final))
        for position in self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]:
             is_final = False
             if position in final_positions_three:
                 final_positions_three.remove(position)
                 is_final = True
             Debug.msg("Position {} is in endposition: {}"
                       .format(position,is_final))
        Debug.msg("Fehlende kleine Blöcke: {}".format(len(final_positions_one)))
        Debug.msg("Fehlende grosse Blöcke: {}".format(len(final_positions_three)))
        
        
        
        # change nested lists to sets of tuples to easily compare them (old version)
        [current_set_b1.add(tuple(element)) for element in self.__challenge[ChallengeKind.StartPosition][BlockKind.One]]
        [current_set_b3.add(tuple(element)) for element in self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]]
        [end_set_b1.add(tuple(element)) for element in self.__challenge[ChallengeKind.EndPosition][BlockKind.One]]
        [end_set_b3.add(tuple(element)) for element in self.__challenge[ChallengeKind.EndPosition][BlockKind.Three]]

        d_1 = current_set_b1 - end_set_b1
        d_3 = current_set_b3 - end_set_b3

        if (len(d_1) == 0 and len(d_3) == 0) or (len(final_positions_one) == 0 and len(final_positions_three) == 0):  #First part before or is of old function and can be removed
            return True
        return False

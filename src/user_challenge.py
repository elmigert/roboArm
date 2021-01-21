#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserChallenge class, which is used to monitor the success of a challenge.
"""
from pathlib import Path
import os
try:
    import configparser
except:
    from six.moves import configparser
    


from enum import Enum

from src.robot_error import ErrorCode, RobotError
from src.debug import Debug


class ChallengeKind(Enum):
    """
    OLD: WIll be removed
    Enum class to distinguish the challenge kinds. Is used to save all position of blocks and manipulation of states. Probably be removed in later stage
    """
    
    BridgeOne = "Brücke 1"
    BridgeTwo = "Brücke 2"
    Beginner = "Anfänger"
    Advanced = 1
    Pro = 3
    StartPosition = 4
    EndPosition = 5
    
    

class Challenge:
    
    blocks = []
    final_pos = []
    block_types = []
    def __init__(self,_name):        
        self.name = _name
        
    def add_start_position(self,block):
        # Adds a block to the start position
        # @block: type: Block
        self.blocks.append(block)   
        
    def add_final_position(self,block):
        # Adds a block to the final position
        # @block: type: Block
        self.final_pos.append(block)
        
    def add_block_type(self,_block_type):
        # Adds a block type with dimension 
        # @_block_type: type: BlockType, holds dimension(x,y) and type (str)
        self.block_types.append(_block_type)

    def valid_block_type(self,_block_type_str):
        # Returns true, if block_type_str exists
        #@_block_type_str: str
        types = [kinds.type.lower() for kinds in self.block_types]
        return _block_type_str.lower() in types
        
        
        
    def final_position_reached(self):
        # Checks, whether all required blocks are in the final position.
        pass
    
    def debug_function(self):
        
        print("Debug function for challenge ",self.name)
        for i in self.blocks:
            print("blocks",i.pos,i.type)
        for i in self.final_pos:
            print("final pos",i.pos,i.type)
        for i in self.block_types:
            print("types",i.type,"dim",i.dimension)

        
        
        
        
    

class BlockKind(Enum): 
    """
    Enum class to distinguish block kinds. OLD
    """
    Null = 0
    One = 1
    Three = 2  # assume direction of 1x3x1 block only in y direction

class BlockType:
    '''
    Different block types and dimensions, NEW: Replaces BlockKind
    '''
    def __init__(self,_type,_dimension):
        '''@Param: 
           type: str, type of the block (name of the type)
            dimension: dimension of the block in [length x,length y] with zero rotation    
        '''
        self.type = _type
        self.dimension = _dimension
class Block:
    coordinate = [None,None,None]
    
   

    def __init__(self,_coordinate,_type,_rotation=None):
        '''
        @Param
            _coordinate: current positino of the block
            _BlockKind: type of the block
            _rotation: current rotation : Not implemented yet
        
        
        '''
        self.coordinate = _coordinate
        self.type = _type
        self.rotation =_rotation
    
    
    @property
    def x(self):
         if self.coordinate[0] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.coordinate[0]
    @property
    def y(self):
         if self.coordinate[1] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.coordinate[1]
         
    @property     
    def z(self):
         if self.coordinate[2] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.coordinate[2]
    
    @property     
    def pos(self):
        return self.coordinate
         
            
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
        

        #Loads all challenges out of the challenges/challenge_init folder. Feel free to define new ones.
        self.__all_challenges = []       
        self.load_challenges()
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
    @staticmethod  
    def challenge_name_path():
        parent_path = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
        path = os.path.join(parent_path,"challenges/challenges_init")
        path_challenges = []
        file_ending = 'ini'
        parser = configparser.ConfigParser()
        challenge_names = []
        for file in os.listdir(path):
            if file.endswith(file_ending):
                path_challenge = os.path.join(path,file)
                path_challenges.append(path_challenge)
                parser.read(path_challenge)
                if parser['CONFIG']['filetype'] == "challenge":
                    challenge_names.append(parser['challenge']['name'])
                else:
                    Debug.error(path_challenge, ' is no valid challenge file. The file is not loaded. Please add challenge to the name in the challenge section.')
        
        return [challenge_names,path_challenges]
 
        
    def load_challenges(self):

        _,challenge_paths = self.challenge_name_path()
        parser = configparser.ConfigParser()
        for path in challenge_paths:
            parser.read(path)
            
            # Generate a challenge template
            challenge = Challenge(parser['challenge']['name'])

            
            # Load block types : Not used
            block_types = parser['challenge']['block_types']
            block_types= block_types.replace('[','')
            block_types= block_types.replace(']','')
            block_types = block_types.split(",")
            block_types = [i.lower() for i in block_types]
            
            # Load block dimensions
            for block_type in parser['Block_Dimensions']:
                dim = parser['Block_Dimensions'][block_type]
                dim = dim.replace('[','')
                dim = dim.replace(']','')
                dim = dim.split(',')
                block_type = block_type.lower()
                if block_type in block_types:
                    challenge.add_block_type(BlockType(block_type,dim))
                else:
                    Debug.error("There is no block type {} (see [Block_Dimensions] in {})".format(block_type,path))
                


            
            # Load start positions
            for key in parser['Start_Position']:
                start_pos = parser['Start_Position'][key]
                start_pos= start_pos.replace('[','')
                start_pos = start_pos.replace(']','')
                start_pos = start_pos.split(",")
                # ToDo: Check i
                if challenge.valid_block_type(start_pos[3]):
                    challenge.add_start_position(Block(start_pos[:3],start_pos[3].lower()))
                else:
                    Debug.error("invalid key of start block: {}".format(start_pos[3] ))
                
                
            # Load final positions
            for key in parser['Final_Position']:
                final_pos = parser['Final_Position'][key]
                final_pos= final_pos.replace('[','')
                final_pos = final_pos.replace(']','')
                final_pos = final_pos.split(",")
                challenge.add_final_position(Block(final_pos[:3],final_pos[3].lower()))
            
            challenge.debug_function()
            #Add the new challenge to the class
            self.__all_challenges.append(challenge)
                

        

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
            # Calculate coordinates below gripper
            coordinates = self.__coordinates.copy()
            Debug.msg('Der Block wird auf der Koordinate {} abgelegt'.format(coordinates[:]))
            # Block coordinate below placed block
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

        # Only check whether the required end position are reached (new version : TE)
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
        
        
        


        if (len(final_positions_one) == 0 and len(final_positions_three) == 0):  #First part before or is of old function and can be removed
            return True
        return False


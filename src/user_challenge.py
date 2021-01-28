#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserChallenge class, which is used to monitor the success of a challenge.
"""
from pathlib import Path
import os
import math
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
    


    

    def __init__(self,_name):  
        self.blocks = []
        self.start_pos = []
        self.final_pos = []
        self.block_types = []
    
        self.init = [False,False,False] # Initialized [start_pos,final_pos,block_types]
        self.name = _name
        
    def add_start_position(self,block):
        # Adds a block to the start position
        # @block: type: Block
        if not self.init[0]:
            self.blocks.append(block)   
            self.start_pos.append(block)
            

    def add_final_position(self,block):
        # Adds a block to the final position
        # @block: type: Block
        if not self.init[1]:
            self.final_pos.append(block)
            
        
    def add_block_type(self,_block_type):
        # Adds a block type with dimension 
        # @_block_type: type: BlockType, holds dimension(x,y) and type (str)
        if not self.init[2]:
            self.block_types.append(_block_type)

    def valid_block_type(self,_block_type_str):
        # Returns true, if block_type_str exists
        #@_block_type_str: str
        types = [kinds.type.lower() for kinds in self.block_types]
        return _block_type_str.lower() in types
        
        
        
    def final_position_reached(self):
        # Checks, whether all required blocks are in the final position.
        pass
    def reset(self):
        self.blocks = self.start_pos
    
    
    def pump_on(self,coordinates):
        # Checks, whether a block is below the pump 
        return self.isBlock([coordinates[:2],coordinates[2]-1]) 
    
    def pump_off(self,coordinates):
        # Checks, whether a block is below the placed block 
        return self.isBlock([coordinates[:2],coordinates[2]-1]) 
        
        
    def isBlock(self,coordinates):
        #CHecks if there is a block at coordinates
        check = False
        print('is coordinate block check: {}'.format(coordinates[:]))
        for block in self.blocks:
            if block.is_on_position([coordinates[:2],coordinates[2]-1]):
                print('There is a block below')
                check = True
                break
        
        return check 
        
    
    def debug_function(self):
        
        print("Debug function for challenge ",self.name)
        for i in self.blocks:
            print("blocks",i.pos,i.type)
        for i in self.final_pos:
            print("final pos",i.pos,i.type)
        for i in self.block_types:
            print("types",i.type,"dim",i.dimension)
    
    def success(self):
        #Checks, whether each of the final position is reached 
        # Note: The wrong rotation is not checked yet
        blocks_total = len(self.final_pos)
        blocks_in_final = 0
        for block_goal in self.final_pos:
            for block_current in self.blocks:
                if block
                

        
        
        
        
    

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
    
   

    def __init__(self,_coordinate,_type,_dimension=None,_rotation=0):
        '''
        @Param
            _coordinate: current center positino of the block (should also work for even blocks)
            
            _coordinates: all occupied full positions
            _BlockKind: type of the block
            _rotation: current rotation: 0: the block is the same as the dimension. Any other number: rotated by this degree anticlockwise
            _dimension: Dimension of the block              
        '''
        
        self.center = _coordinate

        self.type = _type
        self.rotation =_rotation
        self.dimension = _dimension
        
        # Note that this code needs to be adjusted if the width is more than 1 block!
        update_coordinates(self)

    def update_coordinates(self):
        if self.dimension:
            self.coordinates = []
            
            for x_b in range(self.dimension[0]):
                for y_b in range(self.dimension[1]):
                    x = x_b - (self.dimension[0]-1)/2
                    y = y_b - (self.dimension[0]-1)/2
                    r = math.sqrt(x**2 + y**2)
                    angle = atan2(y,x)
                    angle = math.radians(self.rotation) + angle
                    self.coordinates.append([round(self.center[0]+ r*math.cos(angle),1),round(self.center[1] + r*math.sin(angle),1)])
        else:
            self.coordinates = self.center       
        Debug.msg('Transformed  coordinates: {}'.format(self.coordinates[:]))
    
    
    def rotation(self,angle):
        # Rotates the block by angle (degree) anticlockwise around the center (self.center)
        
        self.rotation = angle
        self.update_coordinates()
        
    @property
    def x(self):
         if self.center[0] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.center[0]
    @property
    def y(self):
         if self.center[1] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.centere[1]
         
    @property     
    def z(self):
         if self.center[2] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.center[2]
    
    
    def is_on_position(self,position):
        # Returns true, if a block occupies the position and false othe
        p_a= self.coordinates[0]
        p_b = self.coordinates[-1]
        if ((p_a[0] < position[0] and  position[0]  < p_b[0]) or (p_a[0] > position[0] and  position[0]  > p_b[0]))
            and ((p_a[1] < position[1] and  position[1]  < p_b[1]) or(p_a[1] < position[1] and  position[1]  < p_b[1])):
                return True
        else:
            
            return Falsegit 
    def is_same(self,position,angle=0):
        # Returns true, if the block occupies the position and false otherwise
        if position == self.center and self.rotation= angle or 
        return position in self.coordinates

            
    @property     
    def center(self):
        # Returns the center of the block
        return self.center
         
            
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

        # TODO (ALR): Add objects for blocks, this will work for now. (TE) : Probably use text file to load different Exercises?
        
        # Old: Delete, as soon as the new code is done
        # hard-coded start and end positions of blocks
        '''self.__all_challenges = []       
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
                                                          }'''
        self.__challenge = challenge
        # check if challenge is not challenge kind
        
        
        # NEW
        self.__all_challenges = []       
        self.load_challenges()
        challenge_loaded = False
        for chal in self.__all_challenges:
            print('Challenge name: {} , chal searching {}'.format(chal.name, challenge))
            if chal.name == challenge:
                 self.__challenge = chal
                 print('Challenge %s ist gestartet. Viel Erfolg beim Lösen.' %{challenge})
                 challenge_loaded = True
                 break
        if not challenge_loaded:
            message = "Die Aufgabe  %s kann nicht geladen werden.  Bitte wählen Sie eine   \
                      andere aus."%{challenge}
            raise RobotError(ErrorCode.E0012, message)            
                 
        
        
        
        # OLD - please remove after the new one is working 
        #All challenges which are already implemented 
        '''
        impl_challenges = [ ChallengeKind.Beginner.value,ChallengeKind.BridgeOne.value,ChallengeKind.BridgeTwo.value] 
        if challenge in impl_challenges:
            for item in ChallengeKind:
                if item.value == challenge:
                    self.__challenge = self.__all_challenges[item] 
                    print('Challenge %s ist gestartet. Viel Erfolg beim Lösen.' %{challenge})
                    break
        else:
            message = "Die Aufgabe  %s ist noch nicht implementiert.  Bitte wählen Sie eine andere aus."%{challenge}
            raise RobotError(ErrorCode.E0012, message)
        '''
           

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
        
        for path in challenge_paths:
            parser = configparser.ConfigParser()
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
                    #Debug.msg("Added Dimensions: {} type: {}".format(dim,block_type))
                else:
                    Debug.error("There is no block type {} (see [Block_Dimensions] in {})".format(block_type,path))
            challenge.init[2] = True
                


            
            # Load start positions
            for key in parser['Start_Position']:
                start_pos = parser['Start_Position'][key]
                start_pos= start_pos.replace('[','')
                start_pos = start_pos.replace(']','')
                start_pos = start_pos.split(",")
                # ToDo: Check i

                if challenge.valid_block_type(start_pos[3]):
                    challenge.add_start_position(Block(start_pos[:3],start_pos[3].lower()))
                    #Debug.msg("Added start positions: {} type: {}".format(start_pos[:3],start_pos[3].lower()))
                else:
                    Debug.error("invalid key of start block: {}".format(start_pos[3] ))
            challenge.init[0] = True
                
                
            # Load final positions
            for key in parser['Final_Position']:
                final_pos = parser['Final_Position'][key]
                final_pos= final_pos.replace('[','')
                final_pos = final_pos.replace(']','')
                final_pos = final_pos.split(",")
                if challenge.valid_block_type(final_pos[3]):
                    challenge.add_final_position(Block(final_pos[:3],final_pos[3].lower()))
                    #Debug.msg("Added final positions: {} type: {}".format(final_pos[:3],final_pos[3].lower()))
                else:
                    Debug.error("invalid key of final block: {}".format(final_pos[3] ))
            challenge.init[1] = True
            
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
    
    
        #New code for the challenge: Update block
        # Update position
        if function == robot.position_new:
            self.__coordinates[0] = args[0]
            self.__coordinates[1] = args[1]
        # Update height
        elif function == robot.height_new:
            self.__coordinates[2] = args[0]
        # Check blocks before putting the pump on
        elif function == robot.pump_on:
            self.__challenge.
            if self.__coordinates in self.__challenge[ChallengeKind.StartPosition][BlockKind.One]:
                self.__challenge[ChallengeKind.StartPosition][BlockKind.One].remove(self.__coordinates)
                self.__block = BlockKind.One
            elif self.__coordinates in self.__challenge[ChallengeKind.StartPosition][BlockKind.Three]:
                self.__challenge[ChallengeKind.StartPosition][BlockKind.Three].remove(self.__coordinates)
                self.__block = BlockKind.Three
            else:
                message = "Die Pumpe kann nur aktiviert werden, um einen Block aufzuheben."
                raise RobotError(ErrorCode.E0013, message)
        
        # Robot Pump OFF
        
        # Robot Pump ON
        
        ''' OLD CODE
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
            raise NotImplementedError()'''

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


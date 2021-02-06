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
        self.start_pos = [] # Type: block, the start position of the blocks
        self.final_pos = [] # Type: block, the goal position of the blocks required to achieve
        self.block_types = [] # @_block_type: type: BlockType, holds dimension(x,y) and type (str)
    
        self.init = [False,False,False] # Initialized [start_pos,final_pos,block_types]
        self.name = _name
        self.block_manipulating = None
        
    def add_start_position(self,block):
        # Adds a block to the start position
        # @block: type: Block
        if not self.init[0]:
            self.blocks.append(block)   
            self.start_pos.append(block)
            

    def add_final_position(self,block):
        # Adds a block to the final position : 
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
    
    def get_dim(self,block_type):
        # Gets dimension of the block_type (string). returns false if there is no dimensions available for the blocktype   
        for types in self.block_types:
            if block_type.lower() == types.type.lower():
                return types.dimension
        return [1,1]
        
        
    def final_position_reached(self):
        # Checks, whether all required blocks are in the final position.
        pass
    def reset(self):
        self.blocks = self.start_pos
    
    
    def pump_on(self,coordinates):
        # Checks, whether a block is below the pump 
        if self.getBlock(coordinates):
            # Everything is fine
            return True
        else:
            message = "Die Pumpe kann nur aktiviert werden, um einen Block aufzuheben."
            raise RobotError(ErrorCode.E0013, message)
            
    
    def pump_off(self,coordinates):
        # Checks whether the block can be placed on the coordinates       
        if self.block_manipulating:
            if self.placeBlock(coordinates):
                # THe block could be succesfully places
                return True
            else:
                # ToDo: The pump should be stopped here or somewhere else
                return False
        else:
            message = "Der Roboter trägt momentan keinen oder keinen bekannten Block"
            raise RobotError(ErrorCode.E0014, message)
    def rotate_man_block(self,angle):
        # rotates the block which is currently holdign by angle anticlockwise (degree)
        if self.block_manipulating:
            self.block_manipulating.rotate(angle)
        else:
            message = "Der Roboter trägt momentan keinen Block, welcher rotiert werden kann"
            raise RobotError(ErrorCode.E0014, message)
            return False
        
        
        
    def isBlock(self,coordinates):
        #Checks if there is a block at coordinates
        check = False
        if coordinates[2] >= 0:
            Debug.msg('Is block on coordinate check: {}'.format(coordinates[:]))
            for block in self.blocks:
                if block.is_on_position(coordinates):
                    Debug.msg('Block found on {}'.format(coordinates))
                    check = True
                    break 
            return check
        else:
            return False
    
    def getBlock(self,coordinates):
        #CHecks if there is a block at coordinates
        check = False
        
        Debug.msg('Get block at: {}'.format(coordinates[:]))
        if coordinates[2] == 0:
            Debug.msg("There is only the floor there ")
            return False
        print('Number of blocks: {}'.format(len(self.blocks)))
        for i in range(len(self.blocks)):
            
            if self.blocks[i].is_on_position(coordinates):
                Debug.msg('We got a block!')
                self.block_manipulating = self.blocks[i]
                self.block_manipulating.getBlock(coordinates)
                del self.blocks[i]
                return True
        Debug.msg('We dont got a block!')
        return check 
    
    def placeBlock(self,coordinates):
        # Checks whether the block can be placed
        check = False
        bottom_coordinates = coordinates.copy()
        bottom_coordinates[2] -= 1
        if self.isBlock(coordinates):
            message = 'There is already a block there'
            Debug.msg(message)
            Debug.error(message)
            raise RobotError(ErrorCode.E0015, message)
            return False
        elif coordinates[2] == 1:
            Debug.msg("The block is placed on the floor")
            self.block_manipulating.placeBlock(coordinates)
            self.blocks.append(self.block_manipulating)
            self.block_manipulating = []
            return True
        elif self.isBlock(bottom_coordinates):
            Debug.msg("The block is placed on another block")
            self.block_manipulating.placeBlock(coordinates)
            self.blocks.append(self.block_manipulating)
            self.block_manipulating = []
            return True 
        else:
            # Implement method for bridge block
            test_block = self.block_manipulating # Used to test whether the block can be placed on two points
            test_block.placeBlock(bottom_coordinates)
            possible_coordinates = test_block.get_positions
            print('Possible coordinates {}'.format(possible_coordinates))
            blocks_below = 0
            for cord in possible_coordinates:
                print('Coordinates to check : {}'.format(cord))
                if self.isBlock(cord):
                    blocks_below +=1
                    Debug.msg('There is a block below but not in the center')
            if blocks_below >= 2:
                Debug.msg("The block is placed on multiple other blocks")
                self.block_manipulating.placeBlock(coordinates)
                self.blocks.append(self.block_manipulating)
                self.block_manipulating = []
                return True  
            else:
                message = "Der Block kann nicht in der Luft losgelassen werden. Platziere den Block auf dem Boden oder auf einem anderen Block"
                Debug.error(message)
                raise RobotError(ErrorCode.E0015, message)
        return check 
    
    def debug_function(self):
        
        # Used to print out the loaded challenges or all the content of a challenge
        
        print("Loading challenge ",self.name)
        print("Start blocks: (position, block type)")
        n = 1
        for i in self.start_pos:
            print("{}: pos: {} type: {}, rot: {}".format(n ,i.pos,i.type,i.rotation))
            n += 1
        n = 1
        print("Block goal: (position, block type)")
        for i in self.final_pos:
            print("{}: pos: {} type: {}, rot: {}".format(n ,i.pos,i.type,i.rotation))
            n += 1
        print("Blocks current position: (position, block type)")
        n = 1
        for i in self.blocks:
            print("{}: pos: {} type: {}, rot: {}".format(n ,i.pos,i.type,i.rotation))
            n += 1
        print("Dimension types:")
        for i in self.block_types:
            print("Block type: ",i.type,", Dimension: ",i.dimension)
    
    def success(self):
        # Checks, whether each of the final position is reached 
        # Note: The wrong rotation is not checked yet
        #self.debug_function()
        blocks_total = len(self.final_pos)
        blocks_in_final = 0
        for block_goal in self.final_pos:           
            for block_current in self.blocks:
                if block_current.is_same(block_goal.pos,block_goal.rotation):
                    blocks_in_final = blocks_in_final + 1
        print (' Block in final: {} of {}'.format(blocks_in_final,blocks_total))
        return blocks_in_final == blocks_total

            
                

        
        
        
        
    

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
    def __init__(self,_coordinate,_type,_dimension=[1,1],_rotation=0):
        '''
        @Param
            _coordinate: current center position of the block (should also work for even blocks)
            
            _coordinates: all occupied full positions
            _BlockKind: type of the block
            _rotation: current rotation: 0: the block is the same as the dimension. Any other number: rotated by this degree anticlockwise
            _dimension: Dimension of the block              
        '''

        self.pos_center =_coordinate

        self.type = _type
        self.rotation =_rotation
        self.dimension = _dimension
        
        # Note that this code needs to be adjusted if the width is more than 1 block!
        self.update_coordinates()

    def update_coordinates(self):
        #print('origin: {} dim[0]: {}, range(x_b {}'.format(self.pos, self.dimension[0],range(self.dimension[0])))
        if self.dimension:
            self.coordinates = []   
            for x_b in range(self.dimension[0]):
                for y_b in range(self.dimension[1]):
                    x = x_b - (self.dimension[0]-1)/2
                    y = y_b - (self.dimension[1]-1)/2
                    r = math.sqrt(x**2 + y**2)
                    angle = math.atan2(y,x)
                    # Debug.msg('x {},y{},r{},angle{}, rotation {}'.format(x,y,r,angle,self.rotation))
                    angle = math.radians(self.rotation) + angle 
                    self.coordinates.append([int(round(self.pos_center[0]+ r*math.cos(angle),1)),int(round(self.pos_center[1] + r*math.sin(angle),1)),int(self.pos_center[2])])
        else:
            self.coordinates =  [self.pos_center]       
        Debug.msg('Transformed  coordinates: {}'.format(self.coordinates[:]))
    
    
    def getBlock(self,coordinate):
        # Sets the hold position in relation to the center
        self.hold_position = []
        for i in range(len(coordinate)):
           self.hold_position.append( round(coordinate[i]-self.pos_center[i],1))
        self.hold_angle = self.rotation
    
    def placeBlock(self,coordinate):
        # Updates the coordinates after the placement of the block
        
        r = math.sqrt(self.hold_position[0]**2 + self.hold_position[1]**2)
        angle_dif = math.atan2(self.hold_position[1],self.hold_position[0])
        angle_change = self.rotation-self.hold_angle
        angle = angle_dif + angle_change
        self.pos_center = [round(coordinate[0] +r*math.cos(angle),1),round(coordinate[1] +r*math.sin(angle),1),coordinate[2] ]
        print('Block placed at {}'.format(self.pos_center[:]))
        self.update_coordinates()
        
        
    
    def rotation(self,angle):
        # Set the rotation of the block to angle (degree) anticlockwise around the center (self.center)
        self.rotation = angle
        self.update_coordinates()
        
        
    def rotate(self,angle):
        # Rotates the block by angle (degree) anticlockwise around the center (self.center)
        rot = self.rotation + angle
        while rot > 360 or rot < 0:
            rot = rot - math.copysign(1,rot) * 360
        self.rotation = rot
        
    @property
    def x(self):
         if self.pos_center[0] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.pos_center[0]
    @property
    def y(self):
         if self.pos_center[1] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.pos_center[1]
         
    @property     
    def z(self):
         if self.pos_center[2] == None:
             Debug.error("Coordinate x not set yet")
             return False
         else:
             return self.pos_center[2]
    
    
    def is_on_position(self,position):
        # Returns true, if a block occupies the position and false othe
        p_a= self.coordinates[0]
        p_b = self.coordinates[-1]
        #print('p_a {}, p_b {} position {}'.format(p_a,p_b,position))
        check = [False,False,False]
        for i in range(3):
            check[i] = (p_a[i] <= position[i] and position[i]  <= p_b[i]) or (p_a[i] >= position[i] and position[i]  >= p_b[i])
            if  not check[i]:
                return False
        return True

    def is_same(self,position,angle=0):
        # Returns true, if the block occupies the position and false otherwise
        angle = round(angle)
        while angle > 180:
            angle = angle - 180
        tmp_rot = round(self.rotation)
        while tmp_rot > 180:
            tmp_rot = round(tmp_rot - 180)  
        #print('position block {}, position goal {}, angle block {}, angle goal {}'.format(self.pos_center,position,tmp_rot,angle))
        if position == self.pos_center and tmp_rot == angle:
            return True

            
    @property     
    def pos(self):
        # Returns the center of the block
        return self.pos_center
    @property
    def get_positions(self):
        # Returns all occupied coordinates (one tile space between the coordinates)
        return self.coordinates
         
            
class UserChallenge:
    """
    This class monitors user challenge success.g
    """
    def __init__(self, challenge, start_coordinates):
        """
        Class initialization.
        :param challenge: Kind of challenge to be monitored.
        :type challenge: ChallengeKind, str
        :param start_coordinates: start position and height of robot in user frame [x, y, z]
        :type start_coordinates: list
        """
        




        self.__challenge = challenge
        
        
        #Turns the terminal debuging comments of
        Debug.error_on = True
        Debug.print_on = True
        
        
        # Loads all challenges out of the challenges/challenge_init folder. Feel free to define new ones.
        self.__all_challenges = []       
        self.load_challenges()
        challenge_loaded = False
        for chal in self.__all_challenges:
            #print('Challenge name: {} , chal searching {}'.format(chal.name, challenge))
            if chal.name == challenge:
                 self.__challenge = chal
                 print('Challenge %s ist gestartet. Viel Erfolg beim Lösen.' %{challenge})
                 challenge_loaded = True
                 break
        if not challenge_loaded:
            message = "Die Aufgabe  %s kann nicht geladen werden.  Bitte wählen Sie eine   \
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
        
        for path in challenge_paths:
            parser = configparser.ConfigParser()
            parser.read(path)
            
            # Generate a challenge template
            challenge = Challenge(parser['challenge']['name'])

            
            # Load block types : Not used
            block_types = parser['challenge']['block_types']
            block_types = block_types.replace('[','')
            block_types = block_types.replace(']','')
            block_types = block_types.split(",")
            block_types = [i.lower() for i in block_types]
            
            # Load block dimensions
            for block_type in parser['Block_Dimensions']:
                dim = parser['Block_Dimensions'][block_type]
                dim = dim.replace('[','')
                dim = dim.replace(']','')
                dim = dim.split(',')
                dim = [int(i) for i in dim]
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
                if len(start_pos) == 4:
                    angle = 0
                elif len(start_pos) == 5:
                    angle = int(start_pos[3])
                else:
                    print("Wrong start_position length. Example name = [x,y,z],rotation,type] or name = [x,y,z], type ")
                if challenge.valid_block_type(start_pos[-1]): 
                    dim = challenge.get_dim(start_pos[-1])
                    #print('dim:' ,dim)
                    challenge.add_start_position(Block([int(i) for i in start_pos[:3]],start_pos[-1].lower(),dim,_rotation=angle))
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
                if len(final_pos) == 4:
                    angle = 0
                elif len(final_pos) == 5:
                    angle = int(final_pos[3])
                else:
                    print("Wrong start_position length. Example name = [x,y,z],rotation,type] or name = [x,y,z], type ")
                if challenge.valid_block_type(final_pos[-1]):
                    dim = challenge.get_dim(final_pos[-1])
                    #print('dim:' ,dim)
                    challenge.add_final_position(Block([int(i) for i in final_pos[:3]],final_pos[-1].lower(),dim,_rotation=angle))
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
            self.__challenge.pump_on(self.__coordinates)
        elif function == robot.pump_off:
            coordinates = self.__coordinates.copy()
            Debug.msg('Der Block wird auf der Koordinate {} abgelegt'.format(coordinates[:]))
            self.__challenge.pump_off(coordinates)
        elif function == robot.drehen:
            Debug.msg('Der Block wird um {} Grad gedreht'.format(args[0]))
            self.__challenge.rotate_man_block(args[0])


    def success(self):
        """
        Check if the challenge was successful by comparing the current and end positions of the blocks.
        This function would be a lot nicer if objects were used for blocks/positions... DONE (TE)
        :return: True if end and current position of all blocks is equal
        :rtype: bool
        """
        
        return self.__challenge.success()

   


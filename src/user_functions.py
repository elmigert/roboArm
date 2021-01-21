
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the possible user functions enter into the 
"""
from enum import Enum
    

class FunctionNames(Enum):
    position = 1
    hoehe = 2
    pumpe_an = 3
    pumpe_aus = 4

class UserFunction:
    """
    The possible user functions
    """
    name = []
    
    def __init__(self, name,**args):
        """
        Initialize the function with a name and a function
        
        :@param name: str, a name in the list FunctionNames
        
        """
        
        
        
        '''
                    # generate function mapping
            if function_string == "position":
                if len(arguments) != 2:
                    message = "Bitte geben Sie zwei Koordinaten für eine neue Position an. Bsp.: position(5, 5)"
                    raise RobotError(ErrorCode.E0007, message)
                self.__function_calls.append({"function": robot_handler.position_new, "args": arguments})
            elif function_string == "hoehe":
                if len(arguments) != 1:
                    message = "Bitte geben Sie eine Koordinate für eine neue Hoehe an. Bsp.: hoehe(2)"
                    raise RobotError(ErrorCode.E0008, message)
                self.__function_calls.append({"function": robot_handler.height_new, "args": arguments})
            elif function_string == "pumpe_an":
                if len(arguments) != 0:
                    message = "Die Funktion pumpe_an benötigt kein Argument. Bsp.: pumpe_an()"
                    raise RobotError(ErrorCode.E0009, message)
                self.__function_calls.append({"function": robot_handler.pump_on, "args": arguments})
            elif function_string == "pumpe_aus":
                if len(arguments) != 0:
                    message = "Die Funktion pumpe_aus benötigt kein Argument. Bsp.: pumpe_aus()"
                    raise RobotError(ErrorCode.E0010, message)
                self.__function_calls.append({"function": robot_handler.pump_off, "args": arguments})
            else:
                message = "Die angegebene function: \"" + function_string + "\" ist nicht bekannt."
                raise RobotError(ErrorCode.E0011, message)
                
                
                '''
        if name == FunctionNames.hoehe.name:
            self.hoehe(z)
        elif name == FunctionNames.position.name:
            self.position(x,y)
        elif name == FunctionNames.pumpe_an.name:
            self.pumpe_an()
        elif name == FunctionNames.pumpe_aus.name:
            self.pumpe_aus()
            
    @classmethod
    def hoehe(clc, z):
        pass
    @classmethod
    def position(self,x,y):
        pass
    @classmethod
    def pumpe_an(self):
        pass
    @classmethod
    def pumpe_aus(self):
        pass
        
            
            
            
        # TODO (ALR): The coordinates should not be hardcoded here.


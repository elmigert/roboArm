#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserScript class.
"""
from src.user_functions import FunctionNames

from src.robot_error import ErrorCode, RobotError
from src.robot_handler import RobotHandler
from src.user_challenge import UserChallenge
from src.debug import Debug

class UserScript:
    """
    The UserScript class handles input given by the frontend, checks it and converts it to robot_handler functions.
    """
    # Static stop variable which tells if the commands should be stopped
    stop = False
    def __init__(self, input_string, robot_handler, challenge):
        """
        Initialize UserScript object from frontend input-string.
        :param input_string: string typed by user in UI
        :type input_string: str
        :param robot_handler: RobotHandler object, managing connection to uArm
        :type robot_handler: RobotHandler
        :param challenge: challenge kind
        :type challenge: str
        """

        # Loads the user challenges
        self.__user_challenge = UserChallenge(challenge)
        
        # Loads the commands from the command window
        self.load_commands(input_string,robot_handler)

                
    def load_commands(self,input_string,robot_handler):
        ''' Loads the commands of the command lines in the terminal given by the input_string '''
        # reset arm so values dont change
        robot_handler.reset()
        # remove all spaces
        input_string = input_string.replace(" ", "")
        # split strings at newline, only keep substrings if they are not empty
        line_list = [i for i in input_string.split("\n") if i != ""]

        self.__function_calls = list()
        # TODO (ALR): Refactor into different functions. (TE): Done: Added functions for each function_string
        # map each string to function and argument
        for line in line_list:
            clean_data = UserScript.__cleanup_line(line)
            function_string = clean_data["function_string"]
            arguments = clean_data["arguments"]
            
            if function_string == FunctionNames.hoehe.name:
                self.hoehe(robot_handler,arguments)
            elif function_string == FunctionNames.position.name:
                self.position(robot_handler,arguments)
            elif function_string == FunctionNames.pumpe_an.name:
                self.pumpe_an(robot_handler,arguments)
            elif function_string == FunctionNames.pumpe_aus.name:
                self.pumpe_aus(robot_handler,arguments)
            elif function_string == FunctionNames.drehen.name:
                self.drehen(robot_handler,arguments)
            elif function_string == FunctionNames.test_c.name:
                self.test_c(robot_handler,arguments)
        
        


    @staticmethod
    def __cleanup_line(line):
        """
        Cleanup script line and return function string and argument list.
        :param line: line of editor
        :type line: str
        :return: function string and corresponding argument list
        :rtype: dict[str, list]
        """
        
        
        # get arguments and functions
        argument_begin = line.find("(")
        argument_end = line.find(")")
        # check if function has brackets
        if argument_begin == -1 or argument_end == -1:
            message = "Funktions Argumente müssen mit runden Klammern umgeben werden. Bsp.: position(1, 2) pumpe_an()"
            raise RobotError(ErrorCode.E0006, message)
        elif len(line) -1 > argument_end :
            message = "Funktions Argumente müssen mit Klammern enden und einzeln pro Zeile eingeben werden.  Bsp.: position(1, 2)"
            raise RobotError(ErrorCode.E0006, message)
        function_string = line[:argument_begin]
        argument_string = line[argument_begin + 1:argument_end]
        # TODO (ALR): Error check? (TE): Added int check and additional bracket end check
        if len(argument_string) > 0:
            try:
                arguments = [int(i) for i in argument_string.split(",")]
                for i in arguments:
                    if not str(i).isdigit():
                        message = "Das eingegebene Argument {} ist keine positive, ganze Zahl".format(i)
                        raise RobotError(ErrorCode.E0006,message)            
            except:
                for i in argument_string.split(","):
                    try:
                        int(i) 
                    except:
                        message = "Das eingegebene Argument {} ist keine gültige Zahl".format(i)
                        raise RobotError(ErrorCode.E0006,message)

        else:
            arguments = []

        return {"function_string": function_string, "arguments": arguments}


    def run_script(self, robot_handler):
        """
        Run script functions on robot.
        :return: True if script was sucessful
        :rtype: bool
        """
        # run functions
        for function_call in self.__function_calls:
            function = function_call["function"]
            argument = function_call["args"]
            # call unbound function
            if len(argument) != 0:
                function(argument)
            else:
                function()
            # update user challenge
            self.__user_challenge.record_robot(robot_handler, function, argument)
            if self.stop:
                break
                print('Robot is stopped')
        self.start_robot()
        Debug.msg("All commands executed. Reseting arm and checking challenge victory conditions")
        robot_handler.reset()
        return self.__user_challenge.success()

    @staticmethod
    def reset(robot_handler):
        """
        Reset robot to home position.
        :param robot_handler: RobotHandler object, managing connection to uArm
        :type robot_handler: RobotHandler
        """

        robot_handler.reset()
    @staticmethod
    def stop_robot():
        ''' Sets the robot into stop state, which will stop all commands'''
        UserScript.stop = True
    @staticmethod
    def start_robot():
        ''' resets the stop state. Thus, the commands are not stopped anymore '''
        UserScript.stop = False
        
        
    def reset_challenge(self):
        
        self.__user_challenge.reset_challenge()

    def current_challenge(self):
        ''' Returns the current loaded challenge
        '''
    
        return self.__user_challenge.current_challenge()

        


        

    def hoehe(self,robot_handler, arguments):
        if len(arguments) != 1:
                    message = "Bitte geben Sie eine Koordinate für eine neue Hoehe an. Bsp.: hoehe(2)"
                    raise RobotError(ErrorCode.E0008, message)
        elif arguments[0] > 3:
                    message = "Die eingegebene Höhe ist {}. Bitte geben sie maximal eine Höhe von 3 ein".format(arguments[0])
                    raise RobotError(ErrorCode.E0008, message)
        elif arguments[0] < 0:
                    message = "Der Motor kann nicht unterhalb des Bodens gehen"
                    raise RobotError(ErrorCode.E0008, message)
            
        self.__function_calls.append( {"function": robot_handler.height_new, "args": arguments})
        
        
    def drehen(self,robot_handler,arguments):
        if len(arguments) != 1:
                    message = "Bitte geben Sie nur einen Winkel für die Drehung an: Bsp:  drehen(90)"
                    raise RobotError(ErrorCode.E0100, message)

        self.__function_calls.append({"function": robot_handler.drehen, "args": arguments})

    def test_c(self,robot_handler,arguments):
         
        self.__function_calls.append({"function": robot_handler.test_c, "args": arguments})

    def position(self,robot_handler,arguments):
        if len(arguments) != 2:
                    message = "Bitte geben Sie zwei Koordinaten für eine neue Position an. Bsp.: position(5, 5)"
                    raise RobotError(ErrorCode.E0007, message)
        self.__function_calls.append({"function": robot_handler.position_new, "args": arguments})
  
    def pumpe_an(self,robot_handler,arguments):
        if len(arguments) != 0:
                    message = "Die Funktion pumpe_an benötigt kein Argument. Bsp.: pumpe_an()"
                    raise RobotError(ErrorCode.E0009, message)
        self.__function_calls.append({"function": robot_handler.pump_on, "args": arguments})

    def pumpe_aus(self,robot_handler,arguments):
        if len(arguments) != 0:
                    message = "Die Funktion pumpe_aus benötigt kein Argument. Bsp.: pumpe_aus()"
                    raise RobotError(ErrorCode.E0010, message)
        self.__function_calls.append({"function": robot_handler.pump_off, "args": arguments})

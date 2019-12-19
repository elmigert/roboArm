#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserScript class.
"""

from src.robot_error import ErrorCode, RobotError
from src.robot_handler import RobotHandler


class UserScript:
    """
    The UserScript class handles input given by the frontend, checks it and converts it to robot_handler functions.
    """
    def __init__(self, input_string, robot_handler):
        """
        Initialize UserScript object from frontend input-string.
        :param input_string: string typed by user in UI
        :type input_string: str
        :param robot_handler: RobotHandler object, managing connection to uArm
        :type robot_handler: RobotHandler
        """
        # remove all spaces
        input_string = input_string.replace(" ", "")
        # split strings at newline, only keep substrings if they are not empty
        line_list = [i for i in input_string.split("\n") if i != ""]

        self.__function_calls = list()
        # TODO: Refactor into different function
        # map each string to function and argument
        for line in line_list:
            clean_data = UserScript.__cleanup_line(line)
            function_string = clean_data["function_string"]
            arguments = clean_data["arguments"]

            # generate function mapping
            if function_string == "position_neu":
                if len(arguments) != 2:
                    message = "Bitte geben Sie zwei Koordinaten für eine neue Position an. Bsp.: position_neu(5, 5)"
                    raise RobotError(ErrorCode.E0007, message)
                self.__function_calls.append({"function": robot_handler.position_new, "args": arguments})
            elif function_string == "hoehe_neu":
                if len(arguments) != 1:
                    message = "Bitte geben Sie eine Koordinate für eine neue Hoehe an. Bsp.: hoehe_neu(2)"
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
            message = "Funktions Argumente müssen mit runden Klammern umgeben werden. Bsp.: position_neu(1, 2) pumpe_an()"
            raise RobotError(ErrorCode.E0006, message)
        function_string = line[:argument_begin]
        argument_string = line[argument_begin + 1:argument_end]
        # TODO: Error check?
        if len(argument_string) > 0:
            arguments = [int(i) for i in argument_string.split(",")]
        else:
            arguments = []

        return {"function_string": function_string, "arguments": arguments}

    def run_script(self, robot_handler):
        """
        Run script functions on robot.
        :param robot_handler: RobotHandler object, managing connection to uArm
        :type robot_handler: RobotHandler
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
        # TODO: Add success check here.

    @staticmethod
    def reset(robot_handler):
        """
        Reset robot to home position.
        :param robot_handler: RobotHandler object, managing connection to uArm
        :type robot_handler: RobotHandler
        """
        robot_handler.reset()

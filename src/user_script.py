#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserScript class.
"""


class UserScript:
    """
    The UserScript class handles input given by the frontend, checks it and converts it to robot_handler functions.
    """
    def __init__(self, input_string):
        """
        Initialize UserScript object from frontend input-string.
        :param input_string: string typed by user in UI
        :type input_string: str
        """
        # remove all spaces
        input_string = input_string.replace(" ", "")
        # split strings at newline, only keep substrings if they are not empty
        line_list = [i for i in input_string.split("\n") if i != ""]

        # map each string to function and argument
        for line in line_list:
            # get arguments and functions
            argument_begin = line.find("(")
            argument_end = line.find(")")
            function_string = line[:argument_begin]
            argument_string = line[argument_begin+1:argument_end]
            if len(argument_string) > 0:
                arguments = [int(i) for i in argument_string.split(",")]
            else:
                arguments = None
            pass


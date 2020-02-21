#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the UserChallenge class, which is used to monitor the success of a challenge.
"""

from enum import Enum


class ChallengeKind(Enum):
    Beginner = 0
    Advanced = 1
    Pro = 3


class UserChallenge:
    """
    This class monitors user challenge success.
    """
    def __init__(self, challenge):
        """
        Class initialization.
        """
        self.__all_challenges = dict()
        self.__challenge = challenge

        
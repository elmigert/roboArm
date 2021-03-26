#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:01:26 2021

@author: mp
"""

class Debug:
    print_on = True
    error_on =True

    def change_print(self, print_state, error_state=True):
        '''
        @func
        either turns debug prints on or of
        @param:
            print_state: bool, turns Deubg print on or off
        '''
        self.print_on = print_state
        self.error_on = error_state
        
    @classmethod
    def msg(cls,text):
        if cls.print_on:
            print(text)
        else:
            pass
    @classmethod
    def error(cls,text):
        if cls.error_on:
            print(text)
        else:
            pass
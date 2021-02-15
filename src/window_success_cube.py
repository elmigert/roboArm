#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotEditor class.
"""

from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QApplication

from src.robot_error import RobotError
from src.user_script import UserScript
from src.user_challenge import UserChallenge


class MagicCubeWindow(QWidget):
    """
    Robot Editor Class, defining UI for robot arm project.
    """
    def __init__(self, n_chal_completed,n_chal_required ):
        """
        Initialize editor.
        :param robot_handler: RobotHandler object Handling connection to uArm
        :type robot_handler: RobotHandler
        """
        super(MagicCubeWindow, self).__init__()
        
        # Add the completed/required challenges
        self._n_chal_completed =  n_chal_completed
        self._n_chal_required  = n_chal_required 


        # first horizontal box
        self.__send_button = QPushButton('Senden')
        self.__close_button = QPushButton('Schliessen')

    

        #  horizontal box
        self.__output_console = QLabel()


        self.__init_ui()

        # Info text
        self.challenge_text()
        
    def __init_ui(self):
        # first horizontal box, buttons and drop-down menu
        h_box_1 = QHBoxLayout()
        h_box_1.addWidget(self.__send_button)

        h_box_1.addWidget(self.__close_button)
        h_box_1.addStretch(1)
        
        # Adds Tooltip
        self.__send_button.setToolTip('Sendet den Challengefortschritt zu dem Magic Cube')
        


        # Output Console
        h_box_2 = QHBoxLayout()
        h_box_2.addWidget(self.__output_console)

        # fill vertical box
        self.v_box = QVBoxLayout()
        self.v_box.addLayout(h_box_1)
        self.v_box.addLayout(h_box_2)

        # button connections
        self.__send_button.clicked.connect(self.__send_to_cube)
        self.__close_button.clicked.connect(self.close)

        # layout
        self.setLayout(self.v_box)
        self.setWindowTitle('Magic Cube Kommunikation')

        self.show()




    def __choice_event(self, text):
        """
        Example choice_change event.
        :param text: text of challenge_choice combox
        :type text: str
        """
        self.__output_console.setText(text)
        
    def challenge_text(self):
        
        text1 = '{} von {} Aufgaben erfolgreich absolviert.'.format(self._n_chal_completed,self._n_chal_required)
        if self._n_chal_completed == self._n_chal_required:
            text = text1 + '\nDer Erfolg kann dem Magic Cube gesendet werden.'
        else:
            text = text1 + '\nLeider müssen noch weitere Challenges gelöst werden, um den Erfolg dem Magic Cube zu senden.'
        
        self.write(text)
        

    def write(self, text):
        """
        Write text in output console.
        :param text: text to be written
        :type text: str
        """
        self.__output_console.setText(text)
    def __send_to_cube(self):
        ''' 
        Sends success of the module to the cube. 
        ToDo: Add sending to cube
        '''
        if self._n_chal_completed == self._n_chal_required:
            print('Success sended to cube')
            # ToDO: Implement cube sending
            self.write('Erfolg wird dem Magic Cube gesendet.')
        else:
            self.write('Es ist/sind erst {} von {} Challenge(s) gelöst. Bitte löse zuerste die fehlende(n) Aufgabe(n)'.format(self._n_chal_completed,self._n_chal_required))
        pass
    
    def add_challenges(self):
        challenges,_ = UserChallenge.challenge_name_path()
        return challenges

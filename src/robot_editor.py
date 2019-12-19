#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotEditor class.
"""

from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel

from src.robot_error import RobotError
from src.user_script import UserScript


class RobotEditor(QWidget):
    """
    Robot Editor Class, defining UI for robot arm project.
    """
    def __init__(self, robot_handler):
        """
        Initialize editor.
        :param robot_handler: RobotHandler object Handling connection to uArm
        :type robot_handler: RobotHandler
        """
        super(RobotEditor, self).__init__()

        self.__robot_handler = robot_handler

        # first horizontal box
        self.__run_button = QPushButton('Start')
        self.__reset_button = QPushButton('Zurücksetzen')
        self.__challenge_choice = QComboBox()
        # TODO: read list of challenges from UserChallenge
        self.__challenge_choice.addItems(["Anfänger", "Fortgeschritten", "Experte"])

        # second horizontal box
        self.__text = QPlainTextEdit(self)
        self.__text.resize(800, 800)

        # third horizontal box
        self.__output_console = QLabel()

        self.__init_ui()

    def __init_ui(self):
        """
        Initialize UI.
        """
        # first horizontal box, buttons and drop-down menu
        h_box_1 = QHBoxLayout()
        h_box_1.addWidget(self.__run_button)
        h_box_1.addWidget(self.__reset_button)
        h_box_1.addWidget(self.__challenge_choice)
        h_box_1.addStretch(1)

        # second  horizontal box, line numbering and text editor
        h_box_2 = QHBoxLayout()
        h_box_2.addWidget(self.__text)

        # third horizontal box, output console
        h_box_3 = QHBoxLayout()
        h_box_3.addWidget(self.__output_console)

        # fill vertical box
        v_box = QVBoxLayout()
        v_box.addLayout(h_box_1)
        v_box.addLayout(h_box_2)
        v_box.addLayout(h_box_3)

        # button connections
        self.__run_button.clicked.connect(self.__run_script)
        self.__reset_button.clicked.connect(self.__reset)
        self.__challenge_choice.activated[str].connect(self.__choice_event)

        # layout
        self.setLayout(v_box)
        self.setWindowTitle('Robot Editor')

        self.show()

    def __run_script(self):
        """
        Run script if possible, if not display error message.
        """
        input_string = self.__text.toPlainText()
        try:
            user_script = UserScript(input_string, self.__robot_handler)
            user_script.run_script(self.__robot_handler)
            self.__output_console.setText("Skript wird ausgeführt.")
        except RobotError as error:
            self.__output_console.setText("FEHLER: " + error.message)

    def __reset(self):
        """
        Move robot back to starting position.
        """
        UserScript.reset(self.__robot_handler)
        self.__output_console.setText("Zurücksetzen des Roboters.")

    def __choice_event(self, text):
        """
        Example choice_change event.
        :param text: text of challenge_choice combox
        :type text: str
        """
        self.__output_console.setText(text)

    def write(self, text):
        """
        Write text in output console.
        :param text: text to be written
        :type text: str
        """
        self.__output_console.setText(text)

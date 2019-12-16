#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotEditor class.
"""

import sys

from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel


class RobotEditor(QWidget):
    """
    Robot Editor Class, defining UI for robot arm project.
    """
    def __init__(self):
        """
        Initialize editor.
        """
        super(RobotEditor, self).__init__()

        # first horizontal box
        self.__run_button = QPushButton('Start')
        self.__stop_button = QPushButton('Stop')
        self.__challenge_choice = QComboBox()
        # TODO: read list of challenges from UserChallenge
        self.__challenge_choice.addItems(["Anfänger", "Fortgeschritten", "Experte"])

        # second horizontal box
        self.__text = QPlainTextEdit(self)
        self.__text.resize(800, 800)

        # third horizontal box
        self.__output_console = QLabel()

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        """
        # first horizontal box, buttons and drop-down menu
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(self.__run_button)
        hbox_1.addWidget(self.__stop_button)
        hbox_1.addWidget(self.__challenge_choice)
        hbox_1.addStretch(1)

        # second  horizontal box, line numbering and text editor
        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(self.__text)

        # third horizontal box, output console
        hbox_3 = QHBoxLayout()
        hbox_3.addWidget(self.__output_console)

        # fill vertical box
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)

        # button connections
        self.__run_button.clicked.connect(self.run_script)
        self.__stop_button.clicked.connect(self.stop)
        self.__challenge_choice.activated[str].connect(self.choice_event)


        # layout
        self.setLayout(vbox)
        self.setWindowTitle('Robot Editor')

        self.show()

    def run_script(self):
        """
        Example run function.
        """
        # TODO: Add UserScript / UserChallenge Connection
        self.__output_console.setText(self.__text.toPlainText())

    def stop(self):
        """
        Example stop function.
        """
        self.__output_console.setText("Stop!")

    def choice_event(self, text):
        """
        Example choice_change event.
        :param text: text of challenge_choice combox
        """
        self.__output_console.setText(text)

# app = QApplication(sys.argv)
# writer = RobotEditor()
# sys.exit(app.exec_())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotEditor class.
"""


import os
try:
    import configparser
except:
    from six.moves import configparser
from PyQt5.QtCore import QThread, QSize
from PyQt5.QtGui import QColor,QPixmap
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QTextEdit

from src.robot_error import RobotError
from src.user_script import UserScript
from src.user_challenge import UserChallenge
from src.window_success_cube import MagicCubeWindow

class Thread(QThread):
    ''' Runs a thread for the reset button'''
    
    def __init__(self,robot_handler):
        super(Thread, self).__init__()
        self.robot_handler = robot_handler
    def run(self):
        UserScript.reset(self.robot_handler)  
        QThread.sleep(1)




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
        self.__reset_button = QPushButton('Stop')
        self.__reset_task_button = QPushButton('Aufgabe zurücksetzen')
        self.__magic_cube_button = QPushButton('Magic Cube Kommunikation')
        self.__challenge_choice = QComboBox()
        
        # adds challenge informations to self.challenge_infos (dict) and completes the text challenge info text, sample text and adds the challenges
        self.add_challenges() 
        
        # Allows only one click on the reset button
        self.__running_reset = Thread(self.__robot_handler)
        self.__running_reset.finished.connect(lambda: self.__reset_button.setEnabled(True))
        
        
        


        # second horizontal box
        ## Headers
        self.__label_text = QLabel('Befehlseingabefeld')
        self.__label_challenge_description = QLabel('Aufgabenbeschreibung')    
        ## Text Boxes
        self.__text = QPlainTextEdit(self)
        self.__text.resize(800, 800)
        
        self.__challenge_description = QTextEdit(self)
        self.__challenge_description.resize(400, 800)
        self.__challenge_description.setPlaceholderText('Hier stehen Information über die Aufgabe')
        self.__challenge_description.setReadOnly(True)

        

        # third horizontal box
        self.__output_console = QLabel()
        # General challenge requirements and victory conditions: Will be updated in the loading process of the config.ini file (see self.__init_general_options())
        self.__required_challenges = 2
        self.completed_challenges = []
        
        # Last box
        
        # Adds a logo
        logo_path = 'pictures/logo.png'
        parent_path = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
        path = os.path.join(parent_path,logo_path)
        logo = QPixmap(path)
        logo = logo.scaled(0.4*logo.size())
        self.__logo = QLabel()
        self.__logo.setPixmap(logo)


        self.__init_ui()
        

        
        

        

    def __init_general_options(self):
        '''
        Read the general options out of the config file in the config folder. Add additional changeable parameter in the config file
        '''
        parent_path = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
        path = os.path.join(parent_path,"config/config.ini")
        parser = configparser.ConfigParser()
        parser.read(path)
        
        self.__required_challenges = parser['CHALLENGES']['required_challenges']
      
    def __init_ui(self):
        """
        Initialize UI.
        """
        # first horizontal box, buttons and drop-down menu
        h_box_1 = QHBoxLayout()
        h_box_1.addWidget(self.__run_button)
        h_box_1.addWidget(self.__reset_button)
        h_box_1.addWidget(self.__reset_task_button)
        h_box_1.addWidget(self.__challenge_choice)
        h_box_1.addStretch(1)
        
        



        # second  horizontal box, line numbering and text editor
        h_box_2_label = QHBoxLayout()
        h_box_2_label.addWidget(self.__label_text)
        h_box_2_label.addWidget(self.__label_challenge_description)
        h_box_2 = QHBoxLayout()
        h_box_2.addWidget(self.__text)
        h_box_2.addWidget(self.__challenge_description)

        # third horizontal box, output console
        h_box_3 = QHBoxLayout()
        h_box_3.addWidget(self.__output_console)
        
                
        # fourth horrizontal button, opens cube connection window
        h_box_4 = QHBoxLayout()
        h_box_4.addWidget(self.__magic_cube_button)
        
        # Last Box, label and comment
        h_box_final = QHBoxLayout()
        # easy formating, was to lazy to google
        h_box_final.addStretch(2)
        h_box_final.addWidget(self.__logo)
        
        
        # Adds tooltips
        self.__run_button.setToolTip('Führt den Befehl aus, der in der Textbox eingegeben wurde')
        self.__reset_button.setToolTip('Stopt den Motor und setzt diesen wieder in die Ausgangslage zurück.')
        self.__reset_task_button.setToolTip('Löscht den Fortschritt der aktuellen Challenge.')
        self.__challenge_choice.setToolTip('Wählt eine Challenge aus')
        self.__magic_cube_button.setToolTip('Öffnet ein Fenster, um den aktuellen Fortschritt dem Magic Cube zu senden.')
        
        
        


        # fill vertical box
        v_box = QVBoxLayout()
        v_box.addLayout(h_box_1)
        v_box.addLayout(h_box_2_label)
        v_box.addLayout(h_box_2)
        v_box.addLayout(h_box_3)
        v_box.addLayout(h_box_4)
        v_box.addLayout(h_box_final)
        


        # button connections
        self.__run_button.clicked.connect(self.__run_script)
        self.__reset_button.clicked.connect(self.__reset_button_clicked)
        self.__reset_task_button.clicked.connect(self.__reset_challenge)
        self.__challenge_choice.activated[str].connect(self.__choice_event)
        self.__magic_cube_button.clicked.connect(self.send_to_cube_window)

        # layout
        self.setLayout(v_box)
        self.setWindowTitle('Robot Editor')
        
        
        # Final updates of challenge texts. TO: I could not make multiple lines to work.
        self.__text.setPlaceholderText("Hier können Befehle für den Roboterarm eingegeben werden." 
                                       "z.B. pumpe_an(), position(5,8) oder hoehe(2)")
        self.update_challenge_infos(self.__challenge_choice.currentText())

        self.show()

    def __run_script(self):
        """
        Run script if possible, if not display error message.
        """
        self.__run_button.setEnabled(False)
        input_string = self.__text.toPlainText()
        
        success = False
        if input_string =='':
            self.__output_console.setText("Keine Befehle eingegeben. Bitte gebe Befehle in das Befehleingabefeld ein.")
        else:
            self.__output_console.setText("Skript wird ausgeführt.")
            challenge = self.__challenge_choice.currentText()
            try:
                if hasattr(self, 'user_script'):
                    if self.user_script.current_challenge() == challenge:
                        print('Continue challenge')
                        self.user_script.load_commands(input_string, self.__robot_handler)
                    else:
                        print('Load new challenge')
                        self.user_script = UserScript(input_string, self.__robot_handler, challenge)
                        
                else:
                        print('Load new challenge')
                        self.user_script = UserScript(input_string, self.__robot_handler, challenge)
                        
                success = self.user_script.run_script(self.__robot_handler)
                
                if success == False:
                    self.__output_console.setText("Aufgabe noch nicht erfüllt, versuche es erneut.")
                elif success == 'test':
                    self.__output_console.setText("Befehle ausgeführt. Testmodus.")
                else:
                    # TODO (ALR): Add Magic Cube Wifi toggle here.
                    n = self.challenge_solved(success)
                    self.__output_console.setText("Aufgabe {} erfolgreich ausgeführt. Super! Gelöste Challenges: {} von {}".format(success,n,self.__required_challenges))
                    self.send_to_cube_window()
            except RobotError as error:
                self.__output_console.setText("FEHLER: " + error.message)
                self.__reset()
                
        self.__run_button.setEnabled(True)
    

    def __reset_button_clicked(self):
        ''' The reset function when the reset button is clicked'''
        
        self.__output_console.setText("Zurücksetzen des Roboters.")
        self.__reset()
    def __reset(self):
        """
        Move robot back to starting position.
        """

        if not self.__running_reset.isRunning():          
            self.__reset_button.setEnabled(False)
            self.__running_reset.start()

            
            
    def __reset_challenge(self):
        if hasattr(self, 'user_script'):
            self.user_script.reset_challenge()
            self.__output_console.setText("Löschen des Fortschrittes der Aufgabe")

                  


    def __choice_event(self, text):
        """
        Example choice_change event.
        :param text: text of challenge_choice combox
        :type text: str
        """
        text =self.__challenge_choice.currentText()
        self.update_challenge_infos(text)
        self.__output_console.setText(text)
        
    def add_text_commands(self,text):
        ''' 
        Updates the sample text in the command box
        @text: str, will be filled into the box
        '''
        
        self.__text.setPlainText(text)

    def update_challenge_description(self,text):
        
        self.__challenge_description.setPlainText(text)

    def write(self, text):
        """
        Write text in output console.
        :param text: text to be written
        :type text: str
        """
        self.__output_console.setText(text)
        
    def challenge_solved(self,challenge_name=None):
        '''
        Adds the challenge_name (str) to the solved challenge and updates the number of solved challenges. Returns the number of solved challenges
        '''
        
        if (not challenge_name in self.completed_challenges) and (challenge_name!=None):
            self.completed_challenges.append(challenge_name)
        return len(self.completed_challenges)
        
        
        
        
        
    def send_to_cube_window(self):
        ''' 
        Opens a window to send the success to the cube
        ToDo: Add sending to cube
        '''
        
        print('Open magic cube window')
        self.__magic_cube_window = MagicCubeWindow(self.challenge_solved(),self.__required_challenges)
    
    
    def add_challenges(self):
        ''' 
        Loads the challenges and add the description text, sample text and all the challenges to the dropdown menu
        '''
        
        self.challenge_infos,_ = UserChallenge.challenge_name_path()
        names = self.challenge_infos['names']
        
                
        for name in names:
            self.__challenge_choice.addItems([name])
            
            
    
    def update_challenge_infos(self,challenge_name):
        ''' Updates the challenge description and sample text 
        @challenge_name: The name of the challenge, which is used to update the challenge name
        '''

        names = self.challenge_infos['names']
        if challenge_name in names:
            idx = names.index(challenge_name)
        self.add_text_commands((self.challenge_infos['sample_text'])[idx])

        self.update_challenge_description((self.challenge_infos['description'])[idx])
        
        
   

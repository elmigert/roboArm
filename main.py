#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the main file of the robot_arm project.
"""

import sys

from PyQt5.QtWidgets import QApplication

from src.robot_editor import RobotEditor
from src.robot_handler import RobotHandler
from src.mock_robot_handler import MockRobotHandler


def main():
    """
    Main function of robot_arm project.
    """
    # --- try connecting to robot
    try:
        robot_handler = RobotHandler()
        text = "Verbindung mit uArm erfolgreich!"
    except Exception:
        # if connection failed, connect to mocked robot handler
        robot_handler = MockRobotHandler()
        text = "Verbindung mit uArm fehlgeschlagen!"

    # --- start main loop
    app = QApplication(sys.argv)
    writer = RobotEditor(robot_handler)
    writer.write(text)
    # --- end of main loop
    run = app.exec_()

    # disconnect robot when closing window
    robot_handler.disconnect()
    sys.exit(run)


if __name__ == '__main__':
    main()

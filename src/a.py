import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_handler import RobotHandler

print("starting")

robot = RobotHandler()
print("connected")

robot.disconnect()

print("disconnected")


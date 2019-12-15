import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_handler import RobotHandler
from src.direction_kind import DirectionKind

print("starting")

robot = RobotHandler()
print("connected")

# move
# robot.position_new(5, 5)
# robot.height_new(1)
# robot.height_new(3)
# robot.position_new(6, 10)
# robot.position_new(5, 5)
# robot.height_new(1)
# robot.height_new(3)
# robot.position_new(6, 10)
# robot.position_new(5, 5)
# robot.height_new(1)
# robot.height_new(3)
# robot.position_new(6, 10)
# robot.position_new(5, 5)
# robot.height_new(1)
# robot.height_new(3)
# robot.position_new(6, 10)
# robot.pump_on()
# robot.height_new(2)
# robot.position_new(5, 7)
# robot.height_new(1)
# robot.pump_off()
# robot.height_new(2)
# robot.height_new(1)
# robot.pump_on()
# robot.height_new(3)
# robot.position_new(5, 5)
# robot.rotate_gripper(DirectionKind.Left)
# robot.height_new(1)
# robot.pump_off()
# robot.height_new(3)
# robot.position_new(6, 6)

time.sleep(2)
robot.set_wrist(0)
time.sleep(5)
robot.set_wrist(90)
time.sleep(5)
robot.set_wrist(180)
time.sleep(5)
# robot.set_wrist(270)


robot.disconnect()
print("disconnected")

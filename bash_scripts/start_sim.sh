#!/usr/bin/env bash
# starts RobotEditor program enabling easy use of the uArm

# example use: bash start.sh /home/mp/mp/robot_arm

directory=..

# move to working directory
cd ${directory}

# source virtual environment
source venv/bin/activate

# execute main : Adds extra argument
python3 main.py --sim True

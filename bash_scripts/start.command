#!/usr/bin/env bash
# starts RobotEditor program enabling easy use of the uArm

# We start at current directory and move to the parent directory
cd "`dirname "$0"`"
directory=..
# move to working directory
cd ${directory}

# source virtual environment
source venv/bin/activate

# execute main
python3 main.py

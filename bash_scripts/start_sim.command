#!/usr/bin/env bash

# starts RobotEditor program enabling easy use of the uArm


# Define the directory you want to move to: First line means that we start in the current working directory
cd "`dirname "$0"`"
directory=..

# move to working directory
cd ${directory}

# source virtual environment
source venv/bin/activate

# execute main : Adds extra argument
python3 main.py --sim True

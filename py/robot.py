#!/usr/bin/env python3

"""
robot.py
=========

This file is the main entry point for the robot. RobotPy runs this file
when launched. We load the robot from the bot submodule, necessary so relative
imports work within the bot (e.g. importing subsystems).
"""

import wpilib
from bot import Robot


class Bot(Robot):
    pass

if __name__ == '__main__':
    wpilib.run(Bot)

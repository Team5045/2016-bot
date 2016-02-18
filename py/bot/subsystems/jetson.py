"""
jetson.py
=========

This file contains the code that relays data from the jetson.
"""

from wpilib import SmartDashboard
from wpilib.command import Subsystem


class Jetson(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.sd = SmartDashboard

    def put_value(self, key, value, valueType='value'):
        print(key, value)
        getattr(self.sd, 'put' + valueType.capitalize())(key, value)

    def get_value(self, key, valueType='value'):
        return getattr(self.sd, 'get' + valueType.capitalize())(key)

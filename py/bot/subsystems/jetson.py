"""
jetson.py
=========

This file contains the code that relays data from the jetson.
"""
import ast

from wpilib import SmartDashboard
from wpilib.command import Subsystem


class Jetson(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.sd = SmartDashboard

    def put_value(self, key, value, valueType='value'):
        # print(key, value)
        getattr(self.sd, 'put' + valueType.capitalize())(key, value)

    def get_value(self, key, valueType='value'):
        try:
            if valueType == 'subarray':
                result = ast.literal_eval(self.sd.getString(key))
            else:
                return getattr(self.sd, 'get' + valueType.capitalize())(key)
            return result
        except KeyError:
            return None

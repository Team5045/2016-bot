"""
jetson.py
=========

This file contains the code that relays data from the jetson.
"""
import ast

from wpilib import SmartDashboard
from wpilib.command import Subsystem

from bot.commands.publish_stats_to_jetson import PublishStatsToJetson


class Jetson(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.sd = SmartDashboard

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(PublishStatsToJetson(self.robot))

    def put_value(self, key, value, valueType='value'):
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

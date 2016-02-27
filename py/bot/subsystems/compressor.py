"""
compressor.py
=========
"""

import wpilib
from wpilib.command import Subsystem

from bot.commands.update_compressor_state import UpdateCompressorState
from bot import config


class Compressor(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.compressor = wpilib.Compressor()

        # Enable compressor by default
        self.robot.jetson.put_value(config.COMPRESSOR_DASHBOARD_KEY, True,
                                    valueType='boolean')

    @property
    def is_enabled(self):
        return self.compressor.enabled()

    def start(self):
        self.compressor.start()

    def stop(self):
        self.compressor.stop()

    def check_and_update_state(self):
        if self.robot.jetson.get_value(config.COMPRESSOR_DASHBOARD_KEY,
                                       valueType='boolean'):
            self.start()
        else:
            self.stop()

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(UpdateCompressorState(self.robot))

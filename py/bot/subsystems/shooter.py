"""
intake.py
=========
"""

import wpilib
from wpilib.command import Subsystem

from bot import config


class Shooter(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.shooter_motor = wpilib.Talon(config.SHOOTER_MOTOR)
        self.shooter_motor.setInverted(False)

    def run(self, speed=0.95):
        self.shooter_motor.set(speed)

    def stop(self):
        self.shooter_motor.set(0)

    # MACRO record/replay support implemented in get_state()
    # and restore_state() methods

    def get_state(self):
        return {
            'shooter_motor': self.shooter_motor.get()
        }

    def restore_state(self, state):
        self.shooter_motor.set(state['shooter_motor'])

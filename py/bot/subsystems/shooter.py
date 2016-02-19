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

    def run(self, speed=1):
        print('running shooter')
        self.shooter_motor.set(speed)

    def stop(self):
        print('stopping shooter')
        self.shooter_motor.set(0)

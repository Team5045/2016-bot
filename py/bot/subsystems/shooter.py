"""
intake.py
=========
"""

import wpilib
from wpilib.command import Subsystem
from wpilib.timer import Timer

from bot import config

SPEED = 0.95
TIME_TO_ACCELERATE = 1.25  # Seconds


class Shooter(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.shooter_motor = wpilib.Talon(config.SHOOTER_MOTOR)
        self.shooter_motor.setInverted(False)

        self.time_started = None

    def run(self, speed=SPEED):
        self.shooter_motor.set(speed)
        if not self.time_started:
            self.time_started = Timer.getFPGATimestamp()

    def stop(self):
        self.shooter_motor.set(0)
        self.time_started = None

    def is_ready_to_shoot(self):
        return self.time_started and \
            Timer.getFPGATimestamp() - self.time_started > TIME_TO_ACCELERATE

    # MACRO record/replay support implemented in get_state()
    # and restore_state() methods

    def get_state(self):
        return {
            'shooter_motor': self.shooter_motor.get()
        }

    def restore_state(self, state):
        self.shooter_motor.set(state['shooter_motor'])

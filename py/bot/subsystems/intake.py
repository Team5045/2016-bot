"""
intake.py
=========
"""

import wpilib
from wpilib.command import Subsystem

from bot import config
from bot.utils.controlled_solenoid import ControlledSolenoid


class Intake(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.intake_solenoid = ControlledSolenoid(config.INTAKE_SOLENOID_FW,
                                                  config.INTAKE_SOLENOID_BW)

        self.intake_motor = wpilib.Talon(config.INTAKE_MOTOR)
        self.intake_motor.setInverted(False)

        self.boulder_limit_switch = wpilib.DigitalInput(
            config.INTAKE_LOADED_LIMIT_SWITCH)

    def toggle(self):
        self.intake_solenoid.toggle()

    def deploy(self):
        self.intake_solenoid.deploy()

    def retract(self):
        self.intake_solenoid.retract()

    def run_with_controller(self, controller):
        speed = -controller.getLeftY()
        self.run(speed)

    def run(self, speed=1):
        self.intake_motor.set(speed)

    def stop(self):
        self.intake_motor.set(0)

    @property
    def has_boulder_loaded(self):
        return self.boulder_limit_switch.get()

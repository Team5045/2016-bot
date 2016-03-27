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
        self.intake_motor.setInverted(True)

        self.boulder_limit_switch = wpilib.DigitalInput(
            config.INTAKE_LOADED_LIMIT_SWITCH)

        self.boulder_reached_limit_switch = False

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

    def mark_boulder_as_unloaded(self):
        # The intake runs so fast that occassionally the boulder
        # will roll all the way past the limit switch before we
        # have a chance to stop it; i.e., boulder_loaded is briefly
        # toggled, but the motors go a bit longer, so when we next
        # check, the boulder is no longer loaded (since it rolls
        # away from the switch). So we offer a sort of cachey way
        # to track it instead. Methods that "remove" the boulder from
        # the bot (shoot + outtake) manually call this function.
        self.boulder_reached_limit_switch = False

    @property
    def has_boulder_loaded(self):
        if not self.boulder_limit_switch.get():
            self.boulder_reached_limit_switch = True
        return self.boulder_reached_limit_switch

    # MACRO record/replay support implemented in get_state()
    # and restore_state() methods

    def get_state(self):
        return {
            'intake_solenoid': self.intake_solenoid.get(),
            'intake_motor': self.intake_motor.get()
        }

    def restore_state(self, state):
        self.intake_solenoid.set(state['intake_solenoid'])
        self.intake_motor.set(state['intake_motor'])

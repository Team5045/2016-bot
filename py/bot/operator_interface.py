"""
operator_interface.py
=========

This file contains the OperatorInterface class, which stores references
to controllers and also is responsible for linking commands to buttons.
"""

from wpilib.buttons import JoystickButton

from bot import config
from bot.utils.buttoned_xbox_controller import ButtonedXboxController
from bot.commands import intake, outtake, shoot, toggle_intake, \
    toggle_driver_direction


class OperatorInterface(object):

    def __init__(self, robot):
        self.robot = robot

        # Controller-level access; used for variable drive/etc.

        self.drive_controller = ButtonedXboxController(
            config.OI_DRIVE_CONTROLLER)

        self.operator_controller = ButtonedXboxController(
            config.OI_OPERATOR_CONTROLLER)

        # Command-level control; used for commands that are simply toggled.

        JoystickButton(self.drive_controller, config.OI_INTAKE) \
            .whileHeld(intake.Intake(self.robot))

        JoystickButton(self.drive_controller, config.OI_OUTTAKE) \
            .whileHeld(outtake.Outtake(self.robot))

        JoystickButton(self.drive_controller, config.OI_SHOOT) \
            .whenReleased(shoot.Shoot(self.robot))

        JoystickButton(self.drive_controller, config.OI_TOGGLE_INTAKE) \
            .toggleWhenPressed(toggle_intake.ToggleIntake(self.robot))

        JoystickButton(self.drive_controller, config.OI_TOGGLE_CAMERA) \
            .toggleWhenPressed(
                toggle_driver_direction.ToggleDriverDirection(self.robot))

    def get_drive_controller(self):
        return self.drive_controller

    def get_operator_controller(self):
        return self.operator_controller

"""
operator_interface.py
=========

This file contains the OperatorInterface class, which stores references
to controllers and also is responsible for linking commands to buttons.
"""

from wpilib import Joystick
from wpilib.buttons import JoystickButton, NetworkButton

from bot import config
from bot.utils.buttoned_xbox_controller import ButtonedXboxController
from bot.commands import intake, outtake, shoot, toggle_intake, \
    toggle_driver_direction, auto_align, record_macro, play_macro


class OperatorInterface(object):

    def __init__(self, robot):
        self.robot = robot

        # DRIVE CONTROLLER

        self.drive_controller = ButtonedXboxController(
            config.OI_DRIVE_CONTROLLER)

        JoystickButton(self.drive_controller, config.OI_INTAKE) \
            .whileHeld(intake.Intake(self.robot))

        JoystickButton(self.drive_controller, config.OI_OUTTAKE) \
            .whileHeld(outtake.Outtake(self.robot))

        JoystickButton(self.drive_controller, config.OI_AUTO_ALIGN) \
            .toggleWhenPressed(auto_align.AutoAlign(self.robot))

        JoystickButton(self.drive_controller, config.OI_SHOOT) \
            .whenReleased(shoot.Shoot(self.robot))

        JoystickButton(self.drive_controller, config.OI_TOGGLE_INTAKE) \
            .whenPressed(toggle_intake.ToggleIntake(self.robot))

        JoystickButton(self.drive_controller, config.OI_TOGGLE_CAMERA) \
            .whenPressed(
                toggle_driver_direction.ToggleDriverDirection(self.robot))

        # OPERATOR CONTROLLER

        self.operator_controller = ButtonedXboxController(
            config.OI_OPERATOR_CONTROLLER)

        JoystickButton(self.operator_controller, config.OI_INTAKE) \
            .whileHeld(intake.Intake(self.robot))

        JoystickButton(self.operator_controller, config.OI_OUTTAKE) \
            .whileHeld(outtake.Outtake(self.robot))

        JoystickButton(self.operator_controller, config.OI_AUTO_ALIGN) \
            .toggleWhenPressed(auto_align.AutoAlign(self.robot))

        JoystickButton(self.operator_controller, config.OI_SHOOT) \
            .whenReleased(shoot.Shoot(self.robot))

        JoystickButton(self.operator_controller, config.OI_TOGGLE_INTAKE) \
            .whenPressed(toggle_intake.ToggleIntake(self.robot))

        # JETSON/DASHBOARD CONTROLLER

        NetworkButton(config.OI_MACRO_TABLE, config.OI_MACRO_RECORD) \
            .whenPressed(record_macro.RecordMacro(self.robot))

        NetworkButton(config.OI_MACRO_TABLE, config.OI_MACRO_PLAY) \
            .whenPressed(play_macro.PlayMacro(self.robot,
                                              jetson_selected=True))

    def get_drive_controller(self):
        return self.drive_controller

    def get_operator_controller(self):
        return self.operator_controller

    def set_controller_rumble(self, level):
        for controller in [self.drive_controller, self.operator_controller]:
            controller.setRumble(Joystick.RumbleType.kLeftRumble_val, level)
            controller.setRumble(Joystick.RumbleType.kRightRumble_val, level)

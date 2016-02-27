"""
drive_train.py
=========

This file contains the drive train subsystem, which is responsible for --
you guessed it -- driving the robot.
"""

import wpilib
from wpilib.command import Subsystem

from bot import config
from bot.commands.drive_with_controller import DriveWithController


class DriveTrain(Subsystem):

    DRIVE_MODE = 'tank'

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.front_left_motor = wpilib.CANTalon(
            config.DRIVE_FRONT_LEFT_MOTOR)
        self.rear_left_motor = wpilib.CANTalon(
            config.DRIVE_REAR_LEFT_MOTOR)
        self.front_right_motor = wpilib.CANTalon(
            config.DRIVE_FRONT_RIGHT_MOTOR)
        self.rear_right_motor = wpilib.CANTalon(
            config.DRIVE_REAR_RIGHT_MOTOR)

        # Configure drive train
        self.drive_train = wpilib.RobotDrive(
            frontLeftMotor=self.front_left_motor,
            rearLeftMotor=self.rear_left_motor,
            frontRightMotor=self.front_right_motor,
            rearRightMotor=self.rear_right_motor
        )
        self.drive_train.setSensitivity(config.DRIVE_SENSITIVITY)
        self.drive_train.setMaxOutput(config.DRIVE_MAX_SPEED)

        # Configure encoders
        self.right_encoder = wpilib.Encoder(config.DRIVE_RIGHT_ENCODER_A,
                                            config.DRIVE_RIGHT_ENCODER_B)
        self.right_encoder.setDistancePerPulse(
            config.DRIVE_ENCODER_DISTANCE_PER_PULSE)

        self.left_encoder = wpilib.Encoder(config.DRIVE_LEFT_ENCODER_A,
                                           config.DRIVE_LEFT_ENCODER_B,
                                           reverseDirection=True)
        self.left_encoder.setDistancePerPulse(
            config.DRIVE_ENCODER_DISTANCE_PER_PULSE)

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(DriveWithController(self.robot))

    def drive(self, speed, curve=0):
        self.drive_train.drive(speed, curve)

    def drive_with_controller(self, controller):
        if self.DRIVE_MODE == 'arcade':
            speed = -controller.getLeftY()
            turn_radius = -controller.getRightX()

            # Invert direction if driver set
            driver_direction = self.robot.driver_direction_chooser \
                .get_selected()

            if driver_direction == 'shooting':
                speed = -speed

            self.drive_train.arcadeDrive(speed, turn_radius, True)

        elif self.DRIVE_MODE == 'tank':
            left_speed = -controller.getLeftY()
            right_speed = -controller.getRightY()

            # Invert direction if driver set
            driver_direction = self.robot.driver_direction_chooser \
                .get_selected()

            if driver_direction == 'shooting':
                self.drive_train.tankDrive(-right_speed, -left_speed, True)
            else:
                self.drive_train.tankDrive(left_speed, right_speed, True)

    def reset_encoders(self):
        self.left_encoder.reset()
        self.right_encoder.reset()

    def get_encoder_distance(self):
        return (self.left_encoder.getDistance() +
                self.right_encoder.getDistance()) / 2.0

    def stop(self):
        self.drive(0)

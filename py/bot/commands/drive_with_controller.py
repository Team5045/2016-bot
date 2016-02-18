"""
drive_with_controller.py
=========

The drive with controller command is run automatically by the DriveTrain
subsystem. It listens for drive controller input and drives the robot.
"""

from wpilib.command import Command


class DriveWithController(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

    def initialize(self):
        pass

    def execute(self):
        drive_controller = self.robot.oi.get_drive_controller()
        self.robot.drive_train.drive_with_controller(drive_controller)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

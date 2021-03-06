"""
__init__.py
===========

The main robot class. Yay!
"""

import wpilib
from wpilib.command import Scheduler

from bot import operator_interface
from bot.subsystems import drive_train, intake, shooter, jetson, navx, \
    auto_chooser, driver_direction_chooser, compressor, sonar, vitals, \
    auto_start_chooser, macros, macro_chooser


class Robot(wpilib.IterativeRobot):

    def robotInit(self):
        """This method is run when the robot turns on. Its purpose is to
        initialize the subsystems.
        """

        self.vitals = vitals.Vitals(self)

        self.navx = navx.NavX(self)
        self.jetson = jetson.Jetson(self)

        self.drive_train = drive_train.DriveTrain(self)
        self.intake = intake.Intake(self)
        self.shooter = shooter.Shooter(self)

        self.compressor = compressor.Compressor(self)
        self.sonar = sonar.Sonar(self)

        self.auto_start_chooser = auto_start_chooser.AutoStartChooser(self)
        self.auto_chooser = auto_chooser.AutoChooser(self)
        self.driver_direction_chooser = driver_direction_chooser \
            .DriverDirectionChooser(self)

        self.macros = macros.Macros(self)
        self.macro_chooser = macro_chooser.MacroChooser(self)

        self.oi = operator_interface.OperatorInterface(self)

        # Set up autonomous command selector
        self.autonomous_command = None

    def autonomousInit(self):
        self.autonomous_command = self.auto_chooser.get_selected()
        self.autonomous_command.start()

    def autonomousPeriodic(self):
        Scheduler.getInstance().run()

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def teleopPeriodic(self):
        Scheduler.getInstance().run()

    def disabledInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def disabledPeriodic(self):
        Scheduler.getInstance().run()

if __name__ == '__main__':
    wpilib.run(Robot)

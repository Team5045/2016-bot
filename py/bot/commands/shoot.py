from wpilib.command import Command
from wpilib.timer import Timer

SHOOT_TIMEOUT = 0.75  # Seconds; time for ball to be lifted to shooter and shot


class Shoot(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)
        self.requires(self.robot.shooter)

    def initialize(self):
        self.first_shoot_time = None
        self.robot.intake.mark_boulder_as_unloaded()

    def execute(self):
        self.robot.shooter.run()
        if self.robot.shooter.is_ready_to_shoot():
            self.robot.intake.run()
            if not self.first_shoot_time:
                self.first_shoot_time = Timer.getFPGATimestamp()

    def isFinished(self):
        if not self.first_shoot_time:
            return False
        return Timer.getFPGATimestamp() - self.first_shoot_time > SHOOT_TIMEOUT

    def end(self):
        self.robot.intake.stop()
        self.robot.shooter.stop()

    def interrupted(self):
        self.end()

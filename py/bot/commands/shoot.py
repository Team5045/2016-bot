from wpilib.command import Command

SHOOT_TIMEOUT = 1.5  # Seconds; time for ball to be lifted to shooter and shot


class Shoot(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)
        self.requires(self.robot.shooter)

    def initialize(self):
        self.setTimeout(SHOOT_TIMEOUT)

    def execute(self):
        self.robot.intake.run()
        self.robot.shooter.run()

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.robot.intake.stop()
        self.robot.shooter.stop()

    def interrupted(self):
        self.end()

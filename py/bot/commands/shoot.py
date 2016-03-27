from wpilib.command import Command

SHOOT_TIMEOUT = 2.5  # Seconds; time for ball to be lifted to shooter and shot
TIME_TO_WAIT_TO_SHOOT = 1.25  # Seconds


class Shoot(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)
        self.requires(self.robot.shooter)

    def initialize(self):
        self.setTimeout(SHOOT_TIMEOUT)
        self.robot.intake.mark_boulder_as_unloaded()

    def execute(self):
        self.robot.shooter.run()
        if self.timeSinceInitialized() > TIME_TO_WAIT_TO_SHOOT:
            # Give shooter time to spin up before starting
            self.robot.intake.run()

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.robot.intake.stop()
        self.robot.shooter.stop()

    def interrupted(self):
        self.end()

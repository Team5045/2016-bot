from wpilib.command import Command


class Outtake(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)

    def initialize(self):
        self.robot.intake.mark_boulder_as_unloaded()

    def execute(self):
        self.robot.intake.run(-1)

    def isFinished(self):
        return False  # Run until interrupted

    def end(self):
        self.robot.intake.stop()

    def interrupted(self):
        self.end()

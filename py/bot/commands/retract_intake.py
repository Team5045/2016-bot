from wpilib.command import Command


class RetractIntake(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)
        self.is_finished = False

    def initialize(self):
        self.robot.intake.retract()
        self.is_finished = True

    def end(self):
        pass

    def interrupted(self):
        self.end()

    def isFinished(self):
        return self.is_finished

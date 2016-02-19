from wpilib.command import Command


class Intake(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)

    def initialize(self):
        pass

    def execute(self):
        print('running intake cmd')
        self.robot.intake.run()

    def isFinished(self):
        # Stop running intake once the boulder is loaded;
        # make sure we don't load more than one.
        return False  # self.robot.intake.has_boulder_loaded

    def end(self):
        self.robot.intake.stop()

    def interrupted(self):
        self.end()

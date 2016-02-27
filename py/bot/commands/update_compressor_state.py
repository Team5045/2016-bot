from wpilib.command import Command


class UpdateCompressorState(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.compressor)

    def initialize(self):
        pass

    def execute(self):
        self.robot.compressor.check_and_update_state()

    def isFinished(self):
        return False

    def end(self):
        pass

    def interrupted(self):
        self.end()

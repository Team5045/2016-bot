from wpilib.command import Command


class JustShoot(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.shooter)

    def initialize(self):
        pass

    def execute(self):
        print('shooting')
        self.robot.shooter.run()

    def isFinished(self):
        return False

    def end(self):
        self.robot.shooter.stop()

    def interrupted(self):
        self.end()

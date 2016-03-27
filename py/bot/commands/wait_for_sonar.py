from wpilib.command import Command


class WaitForSonar(Command):

    def __init__(self, robot, distance_gt=0, distance_lt=0):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.sonar)
        self.distance_gt = distance_gt
        self.distance_lt = distance_lt

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        value = self.robot.sonar.get()

        print('waiting for sonar', value)
        if self.distance_gt:
            return value > self.distance_gt
        else:
            return value < self.distance_lt

    def end(self):
        pass

    def interrupted(self):
        self.end()

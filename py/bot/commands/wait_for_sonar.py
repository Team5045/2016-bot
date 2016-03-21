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
        if self.distance_gt:
            return self.robot.sonar.get() > self.distance_gt
        else:
            return self.robot.sonar.get() < self.distance_lt

    def end(self):
        pass

    def interrupted(self):
        self.end()

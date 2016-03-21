from wpilib.command import Command


class Rotate(Command):

    MAX_SPEED = 1  # 0-1 scaled
    TOLERANCE = 2
    K_ERROR_ADJUST = 1 / 70

    def __init__(self, robot, degrees):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.requires(self.robot.navx)
        self.desired_angle = degrees
        self.speed = self.MAX_SPEED

    def initialize(self):
        self.robot.navx.reset()

        if self.desired_angle >= 0:
            self.curve = 1
        else:
            self.curve = -1

        self.error = 0

    def execute(self):
        self.error = self.desired_angle - self.robot.navx.get_yaw()

        speed = self.speed  # * (abs(self.error) / self.error)
        if speed * (self.error * self.K_ERROR_ADJUST) < self.speed:
            speed = speed * (self.error * self.K_ERROR_ADJUST)

        if abs(speed) < 0.7:
            speed = 0.7 * abs(speed) / speed

        print('[auto rotate]', self.error, speed)

        self.robot.drive_train.drive(speed, self.curve)

    def isFinished(self):
        return abs(self.error) <= self.TOLERANCE

    def end(self):
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

from wpilib.command import Command


class Rotate(Command):

    MAX_SPEED = 0.2  # 0-1 scaled
    TOLERANCE = 0.01
    ENCODER_TO_ANGLE_RATIO = -25 / 90  # Encoders distance / angle (degrees)

    def __init__(self, robot, degrees):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.desired_angle = degrees
        self.speed = self.MAX_SPEED

    def initialize(self):
        self.robot.drive_train.reset_encoders()

        if self.desired_angle >= 0:
            self.encoder = self.robot.drive_train.right_encoder
            self.curve = 1
        else:
            self.encoder = self.robot.drive_train.left_encoder
            self.curve = -1

        self.needed_value = (self.ENCODER_TO_ANGLE_RATIO *
                             abs(self.desired_angle))
        self.error = 0

    def execute(self):
        self.error = self.needed_value - self.encoder.getDistance()

        if self.speed * abs(self.error) > self.speed:
            speed = self.speed * (abs(self.error) / self.error)
        else:
            speed = self.speed * self.error

        self.robot.drive_train.drive(speed, self.curve)

    def isFinished(self):
        return abs(self.error) <= self.TOLERANCE

    def end(self):
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

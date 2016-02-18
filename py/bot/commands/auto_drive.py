from wpilib.command import Command


class Drive(Command):

    MAX_SPEED = 0.3  # 0-1 scaled
    TOLERANCE = .5  # Inches
    KP = -1/5

    def __init__(self, robot, distance):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

        self.distance = abs(distance)  # Inches
        self.is_backwards = distance < 0
        self.speed = self.MAX_SPEED
        self.error = 0

    def initialize(self):
        self.robot.drive_train.reset_encoders()

    def execute(self):
        left_distance = self.robot.drive_train.left_encoder.getDistance()
        right_distance = self.robot.drive_train.right_encoder.getDistance()
        self.error = self.distance - \
            self.robot.drive_train.get_encoder_distance()

        if self.speed * self.KP * self.error >= self.speed:
            speed = self.speed
        else:
            speed = self.speed * self.KP * self.error

        self.robot.drive_train.drive(
            speed if not self.is_backwards else -speed,
            (right_distance - left_distance) * 0.25)

    def isFinished(self):
        return abs(self.error) <= self.TOLERANCE

    def end(self):
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

from wpilib.command import Command


class Drive(Command):

    MAX_SPEED = 0.5  # 0-1 scaled
    TOLERANCE = .5  # Inches
    KP = 1/2

    def __init__(self, robot, distance, dont_stop=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.distance = abs(distance)  # Inches
        self.is_backwards = distance < 0
        self.speed = self.MAX_SPEED
        self.error = float('inf')
        self.dont_stop = dont_stop

    def initialize(self):
        print('init!')
        self.robot.drive_train.reset_encoders()

    def execute(self):
        left_distance = self.robot.drive_train.left_encoder.getDistance()
        right_distance = self.robot.drive_train.right_encoder.getDistance()
        self.error = self.distance - \
            abs(self.robot.drive_train.get_encoder_distance())

        if self.speed * self.KP * self.error >= self.speed:
            speed = self.speed
        else:
            speed = self.speed * self.KP * self.error

        print('[auto drive]', left_distance, right_distance,
              speed if not self.is_backwards else -speed, self.error)

        self.robot.drive_train.drive(
            speed if not self.is_backwards else -speed,
            (right_distance - left_distance) * 0.25)

    def isFinished(self):
        if self.dont_stop:
            return False

        print('is finished', abs(self.error) <= self.TOLERANCE)
        return abs(self.error) <= self.TOLERANCE

    def end(self):
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

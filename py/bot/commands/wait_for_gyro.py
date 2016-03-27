from wpilib.command import Command
from wpilib.timer import Timer

TOLERANCE = 5  # degrees


class WaitForGyro(Command):

    """Wait until gyro has desired values for at least duration seconds."""
    def __init__(self, robot, pitch=None, yaw=None, roll=None, duration=0):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.navx)
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

        self.duration = duration
        self.time_gyro_ok = None

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        print('waiting for gyro', self.robot.navx.get_formatted_status())
        finished = True

        if self.pitch is not None:
            if abs(self.pitch - self.robot.navx.get_pitch()) > TOLERANCE:
                finished = False

        if self.yaw is not None:
            if abs(self.yaw - self.robot.navx.get_yaw()) > TOLERANCE:
                finished = False

        if self.roll is not None:
            if abs(self.roll - self.robot.navx.get_roll()) > TOLERANCE:
                finished = False

        print ('is finished gyro', finished)

        if not finished:
            self.time_gyro_ok = None
            return False

        if not self.time_gyro_ok:
            self.time_gyro_ok = Timer.getFPGATimestamp()

        elapsed = Timer.getFPGATimestamp() - self.time_gyro_ok

        print(elapsed)
        return elapsed > self.duration

    def end(self):
        pass

    def interrupted(self):
        self.end()

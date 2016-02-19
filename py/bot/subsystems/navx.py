from wpilib.command import Subsystem

from robotpy_ext.common_drivers.navx.ahrs import AHRS


class NavX(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.navx = AHRS.create_i2c()

    def reset(self):
        self.navx.zeroYaw()

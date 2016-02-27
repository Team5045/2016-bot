from wpilib.command import Subsystem

from robotpy_ext.common_drivers.navx.ahrs import AHRS

from bot.commands.publish_navx_values import PublishNavxValues


class NavX(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.navx = AHRS.create_i2c(port=1, update_rate_hz=40)

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(PublishNavxValues(self.robot))

    def reset(self):
        self.navx.zeroYaw()

    def get_formatted_status(self):
        return 'pitch: {}, yaw: {}, roll: {}'.format(
            self.get_pitch(), self.get_yaw(), self.get_roll())

    def get_pitch(self):
        # Reversed w/ roll due to unusual mounting
        return self.navx.getRoll()

    def get_roll(self):
        # Reversed w/ pitch due to unusual mounting
        return self.navx.getPitch()

    def get_yaw(self):
        return self.navx.getYaw()

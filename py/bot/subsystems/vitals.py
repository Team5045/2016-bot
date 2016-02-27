from wpilib.command import Subsystem
from wpilib import PowerDistributionPanel

LOW_VOLTAGE_LIMIT = 10  # Out of 12v theoretical max


class Vitals(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.pdp = PowerDistributionPanel()

    def get_voltage(self):
        return self.pdp.getVoltage()

    def is_low_voltage(self):
        return self.get_voltage() < LOW_VOLTAGE_LIMIT

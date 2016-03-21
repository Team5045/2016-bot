"""
sonar.py
=========
"""

from wpilib.command import Subsystem
from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth

from bot import config


class Sonar(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.sensor = MaxSonarEZPulseWidth(config.SONAR_PORT)

    def get(self):
        return self.sensor.get() * 12  # Convert to inches

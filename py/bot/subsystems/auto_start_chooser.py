from wpilib import SendableChooser
from wpilib.command import Subsystem

from bot import config


class AutoStartChooser(Subsystem):

    POSITIONS = [
        [1, '1 - Low bar'],
        [2, '2'],
        [3, '3 - Audience selected'],
        [4, '4'],
        [5, '5']
    ]

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.chooser = SendableChooser()

        for index, description in self.POSITIONS:
            if index == 0:
                self.chooser.addDefault(description, index)
            else:
                self.chooser.addObject(description, index)

        self.robot.jetson.put_value(config.MISC_AUTO_START_DASHBOARD_KEY,
                                    self.chooser, 'data')

    def get_selected(self):
        return self.chooser.getSelected()

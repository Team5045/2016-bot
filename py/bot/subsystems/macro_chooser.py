from wpilib import SendableChooser
from wpilib.command import Subsystem

from bot import config


class MacroChooser(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.chooser = SendableChooser()

        self.refresh_options()

    def refresh_options(self):
        for i, macro in enumerate(self.robot.macros.get_recorded_macros()):
            if i == 0:
                self.chooser.addDefault(macro, macro)
            else:
                self.chooser.addObject(macro, macro)

        self.robot.jetson.put_value(config.MACROS_DASHBOARD_KEY,
                                    self.chooser, 'data')

    def get_selected(self):
        return self.chooser.getSelected()

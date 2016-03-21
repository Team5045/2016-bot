from wpilib.command import CommandGroup

from .command_utils import RunCommandUntilCommandFinished
from .wait_for_sonar import WaitForSonar
from .auto_drive import Drive


class AutoCross(CommandGroup):

    def __init__(self, robot):
        print('init autocross')
        super().__init__(robot)
        self.addParallel(RunCommandUntilCommandFinished(
            run=Drive(robot, distance=float('inf'), speed=0.6),
            watch=WaitForSonar(robot, distance_gt=30)
        ))

    def initialize(self):
        print('initialize autocross')

    def execute(self):
        print('exec autocross')

    def isFinished(self):
        return super().isFinished()

    def end(self):
        pass

    def interrupted(self):
        pass

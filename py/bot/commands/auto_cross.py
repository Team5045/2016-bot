from wpilib.command import CommandGroup

from .command_utils import RunCommandUntilCommandFinished
from .wait_for_gyro import WaitForGyro
from .wait_for_sonar import WaitForSonar
from .auto_drive import Drive


class AutoCross(CommandGroup):

    def __init__(self, robot):
        super().__init__(robot)
        # self.addSequential(JustShoot(robot))
        self.addSequential(RunCommandUntilCommandFinished(robot,
            run=Drive(robot, distance=float('inf'), speed=-0.6),
            watch=[
                WaitForGyro(robot, pitch=0),
                WaitForSonar(robot, distance_gt=70)
            ]
        ))

    def isFinished(self):
        return super().isFinished()

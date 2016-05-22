from wpilib.command import CommandGroup

from bot.commands.shoot import Shoot
from bot.commands.auto_align import AutoAlign


class AutoAlignAndShoot(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.addSequential(AutoAlign(robot,
                                     search_for_target=True,
                                     alignment_iterations=3,
                                     start_shooter_when_close=True))
        self.addSequential(Shoot(robot))

    def isFinished(self):
        return super().isFinished()

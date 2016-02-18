from wpilib.command import CommandGroup, Command

from bot.commands.shoot import Shoot
from bot.commands.auto_align import AutoAlign
from bot.commands.auto_drive import Drive
from bot.commands.auto_rotate import Rotate


class NoAutonomous(Command):
    nickname = "Do nothing"

    def __init(self, robot):
        super().init()

    def end(self):
        pass

    def interrupted(self):
        pass

    def isFinished(self):
        return True


class Autonomous(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot


class SpyBotShooterAutonomous(Autonomous):
    nickname = "Start in spy box; shoot"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(Drive(robot, 24))
        self.addSequential(Rotate(robot, -45))
        self.addSequential(AutoAlign(robot))
        self.addSequential(Shoot(robot))

    def end(self):
        pass

    def interrupted(self):
        pass

    def isFinished(self):
        return super().isFinished()


class TouchDefenseAutonomous(Autonomous):
    nickname = "Start in neutral; drive until touching a defense"

    def __init__(self, robot):
        super().__init__(robot)
        # self.addSequential(Drive(robot))

    def end(self):
        pass

    def interrupted(self):
        pass

    def isFinished(self):
        return super().isFinished()

# List of all available autonomous commands provided in file
auto_commands = [NoAutonomous, SpyBotShooterAutonomous,
                 TouchDefenseAutonomous]

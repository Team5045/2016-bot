from wpilib.command import CommandGroup, Command

from bot.commands.shoot import Shoot
from bot.commands.auto_align import AutoAlign
from bot.commands.auto_drive import Drive
from bot.commands.auto_rotate_2 import Rotate
from bot.commands.retract_intake import RetractIntake


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
        # self.addSequential(RetractIntake(robot))
        self.addSequential(Drive(robot, -50))
        self.addSequential(Rotate(robot, -135))
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
        self.requires(self.robot.navx)
        self.addParallel(RetractIntake(robot))
        self.addParallel(Drive(robot, -65, dont_stop=True))

    def initialize(self):
        self.robot.navx.reset()

    def execute(self):
        pass

    def end(self):
        pass

    def interrupted(self):
        pass

    def isFinished(self):
        return super().isFinished()


class CrossDefenseAndShootAutonomous(Autonomous):
    nickname = "Start in neutral; cross defense; shoot boulder"

    def __init__(self, robot):
        super().__init__(robot)
        self.requires(self.robot.navx)
        self.addParallel(RetractIntake(robot))
        self.addParallel(Drive(robot, -60))
        self.addSequential(AutoAlign(robot))
        self.addSequential(Shoot(robot))

    def initialize(self):
        pass

    def execute(self):
        pass

    def end(self):
        pass

    def interrupted(self):
        pass

    def isFinished(self):
        return super().isFinished()

# List of all available autonomous commands provided in file
auto_commands = [NoAutonomous, SpyBotShooterAutonomous,
                 TouchDefenseAutonomous, CrossDefenseAndShootAutonomous]

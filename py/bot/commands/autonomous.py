from wpilib.command import CommandGroup, Command

from bot.commands.shoot import Shoot
from bot.commands.auto_align import AutoAlign
from bot.commands.auto_cross import AutoCross
from bot.commands.auto_drive import Drive
from bot.commands.auto_rotate import Rotate
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

    def isFinished(self):
        return super().isFinished()


class TouchDefenseAutonomous(Autonomous):
    nickname = "Start in neutral; touch defense"

    def __init__(self, robot):
        super().__init__(robot)
        self.requires(self.robot.navx)
        self.addParallel(RetractIntake(robot))
        self.addParallel(Drive(robot, -65, dont_stop=True))

    def initialize(self):
        self.robot.navx.reset()

    def isFinished(self):
        return super().isFinished()


class OldCrossDefenseAutonomous(Autonomous):
    nickname = "[non-navx] Start in neutral; cross defense"

    def __init__(self, robot):
        super().__init__(robot)
        self.addParallel(RetractIntake(robot))
        self.addParallel(Drive(robot, -250, speed=0.6))

    def isFinished(self):
        return super().isFinished()


class CrossDefenseAutonomous(Autonomous):
    nickname = "Start in neutral; cross defense"

    def __init__(self, robot):
        super().__init__(robot)
        self.addParallel(RetractIntake(robot))
        self.addParallel(AutoCross(robot))
        self.addSequential(Drive(robot, -3, speed=0.6))

    def isFinished(self):
        return super().isFinished()


class CrossDefenseAndShootAutonomous(Autonomous):
    nickname = "Start in neutral; cross defense; shoot boulder"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(RetractIntake(robot))
        self.addSequential(Drive(robot, -120, speed=0.6))
        self.addSequential(AutoCross(robot))
        self.addSequential(AutoAlign(robot,
                                     search_for_target=True,
                                     alignment_iterations=3))
        self.addSequential(Shoot(robot))

    def isFinished(self):
        return super().isFinished()

# List of all available autonomous commands provided in file
auto_commands = [CrossDefenseAndShootAutonomous, CrossDefenseAutonomous,
                 NoAutonomous, TouchDefenseAutonomous,
                 OldCrossDefenseAutonomous]

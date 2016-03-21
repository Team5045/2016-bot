from wpilib.command import CommandGroup

from bot.commands.auto_drive import Drive
from bot.commands.auto_rotate import Rotate


class DriveToBatterFromDefense(CommandGroup):

    """For each potential autonomous starting position, the angle to turn to
    and then the distance to drive in order to reach the batter, in the format
    [int() degrees, int() inches].
    """
    INSTRUCTIONS = {
        1: [38, 90],
        2: [38, 90],
        3: [22, 75],
        4: [-11, 68],
        5: [-31, 75]
    }

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.auto_start_chooser)

        self.is_failed = False
        self.starting_position = self.robot.auto_start_chooser.get_selected()

        # Abort if we can't get our starting position
        if not self.starting_position or self.starting_position == 1:
            self.is_failed = True

        angle, distance = self.INSTRUCTIONS[self.starting_position]

        # Note: Made negative since the "front" of the bot is the intake side,
        # but during autonomous we drive with the shooter in front (so as to
        # line us up for the goal eventually)

        self.addSequential(Rotate(self.robot, degrees=-angle))
        self.addSequential(Drive(self.robot, distance=-distance))
        self.addSequential(Rotate(self.robot, degrees=angle))

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return self.is_failed or super().isFinished()

    def end(self):
        pass

    def interrupted(self):
        self.end()

from wpilib.command import Command
from wpilib.timer import Timer

MACRO_LENGTH = 15  # Seconds


class PlayMacro(Command):

    def __init__(self, robot, name=None):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.macros)

        if name:
            self.name = name
        else:
            recorded = self.robot.macros.get_recorded_macros()
            if len(recorded) > 0:
                self.name = self.robot.macros.get_recorded_macros()[-1]
            else:
                self.name = None

        self.setTimeout(MACRO_LENGTH)

    def initialize(self):
        self.start_time = self.robot.macros.get_time()
        self.reader = self.robot.macros.make_macro_reader(self.name)

        for time, state in self.reader.items():
            t_delta = time - \
                (self.robot.macros.get_time() - self.start_time)

            if t_delta > 0:
                Timer.delay(t_delta)

            self.robot.macros.restore_state(state)

            if self.isTimedOut():
                break

    def execute(self):
        pass

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.reader.end()

    def interrupted(self):
        self.end()

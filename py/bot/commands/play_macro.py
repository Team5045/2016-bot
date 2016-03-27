from wpilib.command import Command
from wpilib.timer import Timer

MACRO_LENGTH = 15  # Seconds


class PlayMacro(Command):

    def __init__(self, robot, name=None, jetson_selected=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.macros)
        self.requires(self.robot.macro_chooser)

        self.name = name
        self.jetson_selected = jetson_selected

        self.setTimeout(MACRO_LENGTH)

    def initialize(self):
        if not self.name:
            if self.jetson_selected:
                self.name = self.robot.macro_chooser.get_selected()
            else:
                recorded = self.robot.macros.get_recorded_macros()
                if len(recorded) > 0:
                    self.name = self.robot.macros.get_recorded_macros()[-1]
                else:
                    self.name = None

        self.start_time = self.robot.macros.get_time()
        self.reader = self.robot.macros.make_macro_reader(self.name)

        self.robot.macros.mark_playing(True)

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
        self.robot.macros.mark_playing(False)

    def interrupted(self):
        self.end()

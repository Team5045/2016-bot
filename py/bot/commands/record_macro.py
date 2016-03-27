import datetime

from wpilib.command import Command

MACRO_LENGTH = 15  # Seconds


class RecordMacro(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.macros)
        self.requires(self.robot.macro_chooser)
        self.setTimeout(MACRO_LENGTH)

    def initialize(self):
        self.start_time = self.robot.macros.get_time()
        formatted_start_time = datetime.datetime.now().isoformat()
        self.writer = self.robot.macros.make_macro_writer(
            name=formatted_start_time)

        self.robot.macros.mark_recording(True)

    def execute(self):
        self.writer.write(
            time=self.robot.macros.get_time() - self.start_time,
            state=self.robot.macros.get_state()
        )

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.writer.end()
        self.robot.macros.mark_recording(False)
        self.robot.macro_chooser.refresh_options()

    def interrupted(self):
        self.end()

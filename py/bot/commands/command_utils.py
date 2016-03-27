from wpilib.command import CommandGroup


class RunCommandUntilCommandsFinished(CommandGroup):

    """
    Arguments:
        run   - the command to run
        watch - the command(s) that, when finished, triggers the first command
                to stop running
    """
    def __init__(self, robot, run, watch):
        super().__init__(robot)
        self.addSequential(run)
        if type(watch) != list:
            watch = [watch]

        for c in watch:
            self.addParallel(c)

        self.watch = watch

        self.is_finished = False

    def initialize(self):
        pass

    def execute(self):
        is_finished = True

        for c in self.watch:
            if not c.isFinished():
                is_finished = False

        self.is_finished = is_finished

    def isFinished(self):
        return self.is_finished

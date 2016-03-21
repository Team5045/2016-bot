from wpilib.command import CommandGroup


class RunCommandUntilCommandFinished(CommandGroup):

    """
    Arguments:
        run   - the command to run
        watch - the command that, when finished, triggers the first command
                to stop running
    """
    def __init__(self, run, watch):
        super().__init__()
        self.run = run
        self.watch = watch
        self.addParallel(self.run)
        self.addParallel(self.watch)

    def initialize(self):
        pass

    def execute(self):
        print('exec rununtil')

    def isFinished(self):
        return self.watch.isFinished()

    # # def end(self):
    # #     pass

    # def interrupted(self):
    #     self.end()

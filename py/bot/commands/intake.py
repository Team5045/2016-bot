from wpilib.command import Command


class Intake(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.intake)

    def initialize(self):
        pass

    def execute(self):
        if not self.robot.intake.has_boulder_loaded:
            self.robot.intake.run()
            self.robot.oi.set_controller_rumble(0)
        else:
            self.robot.intake.stop()
            self.robot.oi.set_controller_rumble(1)

    def isFinished(self):
        return False

    def end(self):
        self.robot.intake.stop()
        self.robot.oi.set_controller_rumble(0)

    def interrupted(self):
        self.end()

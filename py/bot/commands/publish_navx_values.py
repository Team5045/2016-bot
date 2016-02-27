from wpilib.command import Command


class PublishNavxValues(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.navx)
        self.requires(self.robot.jetson)

    def initialize(self):
        pass

    def execute(self):
        self.robot.jetson.put_value('navx_data',
                                    self.robot.navx.get_formatted_status(),
                                    valueType='string')
        self.robot.jetson.put_value('encoders',
                                    self.robot.drive_train.get_encoder_distance(),
                                    valueType='number')

    def isFinished(self):
        return False

    def end(self):
        pass

    def interrupted(self):
        self.end()

from wpilib.command import Command


class PublishStatsToJetson(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.navx)
        self.requires(self.robot.jetson)

    def initialize(self):
        pass

    def execute(self):
        navx = self.robot.navx.get_formatted_status()
        self.robot.jetson.put_value('navx_data', navx, valueType='string')

        encoder = self.robot.drive_train.get_encoder_distance()
        self.robot.jetson.put_value('encoders', encoder, valueType='number')

        sonar = self.robot.sonar.get()
        self.robot.jetson.put_value('sonar', sonar, valueType='number')

    def isFinished(self):
        return False

    def end(self):
        pass

    def interrupted(self):
        self.end()

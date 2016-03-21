from wpilib.command import CommandGroup

TARGET_FOUND = 'target_found'
DISTANCE_AWAY = 'target_details--distance_away'
COORDS = 'target_details--coords'

SKEW_TOLERANCE = 0.1  # How "skewed" the goal can be to move on

ACTUAL_GOAL_WIDTH_IN_INCHES = 20
GOAL_CENTER = (0.5, 0.3)  # Target location to center the target
CENTERING_X_TOLERANCE = 0.02
CENTERING_Y_TOLERANCE = 0.02

MAX_DISTANCE = 30  # Inches
MIN_DISTANCE = 20


class AutoAlign(CommandGroup):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.requires(self.robot.vitals)

    def initialize(self):
        self.is_aligned = False
        self.is_failed = False

        self.phase = 'centering-x'

    def do_things(self, coords, distance_away=None):
        """There are a number of different steps to alignment. This function
        uses certain tolerances to progress through the steps and basically
        return the drive instructions along any step of the way. It's slightly
        magical...but hey, it works.
        """

        # Coords given in tuple form (x, y); these are indices
        x = 0
        y = 1

        top_left = coords[0]
        top_right = coords[1]
        bottom_right = coords[2]
        bottom_left = coords[3]
        center = [(top_right[x] + top_left[x] + bottom_right[x] +
                   bottom_left[x]) / 4,
                  (top_right[y] + top_left[y] + bottom_right[y] +
                   bottom_left[y]) / 4]

        off_x = GOAL_CENTER[x] - center[x]
        off_y = GOAL_CENTER[y] - center[y]

        needs_x = abs(off_x) > CENTERING_X_TOLERANCE
        needs_y = abs(off_y) > CENTERING_Y_TOLERANCE

        if (not needs_x) and (not needs_y):
            self.robot.drive_train.stop()
            print('[auto align] is aligned!')
            self.is_aligned = True
            return

        if needs_x:
            speed = 0.5 * ((abs(off_y) / off_y) if needs_y else 1)
            if abs(off_x) < 0.1:
                speed = 0.3 * ((abs(off_y) / off_y) if needs_y else 1)
            if off_x > 0:
                angle = -0.7 * ((abs(off_y) / off_y) if needs_y else 1)
            elif off_x < 0:
                angle = 0.7 * ((abs(off_y) / off_y) if needs_y else 1)

        else:
            speed = 0.3 * abs(off_y)
            if speed > 0.3:
                speed = 0.3
            elif speed < 0.1:
                speed = 0.1
            speed = speed * abs(off_y) / off_y
            angle = 0

        if not needs_y:
            speed = 0.5 * abs(off_x)
            if speed > 0.6:
                speed = 0.6
            elif speed < 0.4:
                speed = 0.4
            angle = abs(angle) / angle

        print('[auto align]', 'off_x', off_x, 'off_y', off_y, 'speed', speed, 'angle', angle)

        self.robot.drive_train.drive(speed, angle)

    def execute(self):
        self.robot.oi.set_controller_rumble(1)

        # If we lose the target, fail immediately
        if not self.robot.jetson.get_value(TARGET_FOUND, valueType='boolean'):
            self.is_failed = True
            return

        coords = self.robot.jetson.get_value(COORDS, valueType='subarray')
        self.do_things(coords=coords)

    def isFinished(self):
        return self.is_failed or self.is_aligned

    def end(self):
        self.robot.oi.set_controller_rumble(0)
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

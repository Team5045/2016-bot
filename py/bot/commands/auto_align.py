from wpilib.command import CommandGroup

TARGET_FOUND = 'target_found'
DISTANCE_AWAY = 'target_details--distance_away'
COORDS = 'target_details--coords'

SKEW_TOLERANCE = 0.1  # How "skewed" the goal can be to move on

ACTUAL_GOAL_WIDTH_IN_INCHES = 20
GOAL_CENTER = (0.55, 0.25)  # Target location to center the target
CENTERING_X_TOLERANCE = 0.02
CENTERING_Y_TOLERANCE = 0.02

MAX_DISTANCE = 30  # Inches
MIN_DISTANCE = 20


class AutoAlign(CommandGroup):

    def __init__(self, robot, search_for_target=False, alignment_iterations=1):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.requires(self.robot.vitals)
        self.alignment_iterations = 0
        self.search_for_target = search_for_target

    def initialize(self):
        self.number_of_interations_aligned = 0
        self.is_aligned = False
        self.is_failed = False

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
            self.number_of_interations_aligned += 1
            print('[auto align] iterations aligned += 1')

            if self.number_of_interations_aligned >= self.alignment_iterations:
                print('[auto align] is aligned!')
                self.is_aligned = True

            return

        if needs_x:
            speed = 0.3 if abs(off_x) < 0.1 else 0.4
            speed = speed * ((abs(off_y) / off_y) if needs_y else 1)
            angle = 0.7 * ((abs(off_y) / off_y) if needs_y else 1)
            angle = angle * (-1 if off_x > 0 else 1)
        else:
            speed = 0.3 * abs(off_y)
            speed = max(min(speed, 0.3), 0.1)
            speed = speed * abs(off_y) / off_y
            angle = 0

        if not needs_y:
            speed = 0.5 * abs(off_x)
            speed = max(min(speed, 0.6), 0.4)
            angle = abs(angle) / angle

        print('[auto align]',
              'off_x', off_x, 'off_y', off_y, 'speed', speed, 'angle', angle)

        self.robot.drive_train.drive(speed, angle)

    def execute(self):
        self.robot.oi.set_controller_rumble(1)

        if not self.robot.jetson.get_value(TARGET_FOUND, valueType='boolean'):
            if self.search_for_target:
                # Just start rotating around looking for the target until we
                # find it... hehe, just keep swimming, just keep swimming.
                self.robot.drive_train.drive(0.6, -1)
            else:
                self.is_failed = True
                return
        else:
            coords = self.robot.jetson.get_value(COORDS, valueType='subarray')
            self.do_things(coords=coords)

    def isFinished(self):
        return self.is_failed or self.is_aligned

    def end(self):
        self.robot.oi.set_controller_rumble(0)
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()

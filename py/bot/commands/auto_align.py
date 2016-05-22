from wpilib.command import CommandGroup

TARGET_FOUND = 'target_found'
COORDS = 'target_details--coords'

GOAL_CENTER = (0.55, 0.25)  # Target location to center the target
CENTERING_X_TOLERANCE = 0.02
CENTERING_Y_TOLERANCE = 0.02

SHOOTER_START_TOLERANCE = 0.1  # % close to final location to rev up shooter

# COMPETITION CARPET
# SPEEDS = {
#     'x_mostly_y': 0.3,
#     'xy': 0.4,
#     'y_only': 0.3,
#     'y_min': 0.1,
#     'y_max': 0.3,
#     'x_only': 0.5,
#     'x_bounds': 0.1
# }

# DEMOS (TUNED)
SPEEDS = {
    'x_mostly_y': 0.3,
    'xy': 0.4,
    'y_only': 0.3,
    'y_min': 0.1,
    'y_max': 0.3,
    'x_only': 0.3,
    'x_bounds': 0.1
}


class AutoAlign(CommandGroup):

    def __init__(self, robot, search_for_target=False, alignment_iterations=1,
                 start_shooter_when_close=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.requires(self.robot.vitals)
        self.alignment_iterations = 0
        self.search_for_target = search_for_target
        self.start_shooter_when_close = start_shooter_when_close

    def initialize(self):
        self.number_of_interations_aligned = 0
        self.is_aligned = False
        self.is_failed = False
        self.within_shooter_start_tolerance = False

    def do_things(self, coords):
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

        # For auto-revving up the shooter; this way the shooter is already
        # spinning when we're ready to shoot the boulder.
        within_x = abs(off_x) < SHOOTER_START_TOLERANCE
        within_y = abs(off_y) < SHOOTER_START_TOLERANCE
        self.within_shooter_start_tolerance = within_x and within_y

        if (not needs_x) and (not needs_y):
            self.robot.drive_train.stop()
            self.number_of_interations_aligned += 1
            print('[auto align] iterations aligned += 1')

            if self.number_of_interations_aligned >= self.alignment_iterations:
                print('[auto align] is aligned!')
                self.is_aligned = True

            return

        if needs_x:
            speed = SPEEDS['x_mostly_y'] if abs(off_x) < 0.1 else SPEEDS['xy']
            speed = speed * ((abs(off_y) / off_y) if needs_y else 1)
            angle = 0.7 * ((abs(off_y) / off_y) if needs_y else 1)
            angle = angle * (-1 if off_x > 0 else 1)
        else:
            speed = SPEEDS['y_only'] * abs(off_y)
            speed = max(min(speed, SPEEDS['y_max']), SPEEDS['y_min'])
            speed = speed * abs(off_y) / off_y
            angle = 0

        if not needs_y:
            speed = SPEEDS['x_only'] * abs(off_x)
            speed = max(min(speed, SPEEDS['x_only'] + SPEEDS['x_bounds']),
                        SPEEDS['x_only'] - SPEEDS['x_bounds'])
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

            # Start the shooter when we're close to the target, so it's ready
            # to shoot the moment we get aligned.
            if self.start_shooter_when_close and \
               self.within_shooter_start_tolerance:
                self.robot.shooter.run()
            else:
                self.robot.shooter.stop()

    def isFinished(self):
        return self.is_failed or self.is_aligned

    def end(self):
        self.robot.oi.set_controller_rumble(0)
        self.robot.drive_train.stop()
        if self.is_failed:
            self.robot.shooter.stop()

    def interrupted(self):
        self.end()

from wpilib.command import CommandGroup

TARGET_FOUND = 'target_found'
DISTANCE_AWAY = 'target_details--distance_away'
COORDS = 'target_details--coords'

SKEW_TOLERANCE = 0.1  # How "skewed" the goal can be to move on

ACTUAL_GOAL_WIDTH_IN_INCHES = 20
GOAL_CENTER = (0.5, 0.5)  # Target location to center the target
CENTERING_X_TOLERANCE = 0.02  # 1%
CENTERING_Y_TOLERANCE = 0.02  # 1%

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

        print('[auto align', center, GOAL_CENTER)

        if self.phase == 'centering-x':
            off = GOAL_CENTER[x] - center[x]
            if abs(off) > CENTERING_X_TOLERANCE:
                # Boost turning speed if low voltage
                if self.robot.vitals.is_low_voltage():
                    speed = 0.75
                else:
                    adjusted = 0.7 * (abs(off) * 2)
                    speed = max(min(adjusted, 0.8), 0.7)
                    # speed = 0.75 * (abs(off) * 2)

                print('[auto align] drive x', speed, -abs(off) / off)
                self.robot.drive_train.drive(speed, -abs(off) / off)
            else:
                self.robot.drive_train.stop()
                self.phase = 'centering-y'

        elif self.phase == 'centering-y':
            off = GOAL_CENTER[y] - center[y]
            if abs(off) > CENTERING_Y_TOLERANCE:
                adjusted = 0.4 * (abs(off) * 2)
                speed = max(min(adjusted, 0.1), 0.2) * abs(off)/off
                print('[auto align] drive y', speed)
                self.robot.drive_train.drive(speed, 0)
            else:
                self.robot.drive_train.stop()
                print('[auto align] is aligned!')
                self.is_aligned = True

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

    # TEMPORARILY DISABLED IN FAVOR OF SIMPLE METHOD ABOVE
    # ------
    # def old_do_things(self, coords, distance_away):
    #     """There are a number of different steps to alignment. This function
    #     uses certain tolerances to progress through the steps and basically
    #     return drive instructions along any step of the way. It's slightly
    #     magical...but hey, it works.
    #     """

    # Coords given in tuple form (x, y); these are indices
    #     x = 0
    #     y = 1

    #     top_left = coords[0]
    #     top_right = coords[1]
    #     bottom_left = coords[2]
    #     bottom_right = coords[3]
    #     center = [((top_left[x] + bottom_left[x]) / 2) +
    #               (top_right[x] + bottom_right[x] / 2),
    #               ((top_left[y] + top_right[y]) / 2) +
    #               (bottom_left[y] + bottom_right[y] / 2)]

    #     if self.phase == 'skew':
    # Find how "skewed" we are on the target based on the difference
    # between the top y coordinates. When we are looking at target
    # straight on, they will be equal. Average top and bottom.
    #         skew = ((top_right[y] - top_left[y]) +
    #                 (bottom_right[y] - bottom_left[y])) / 2

    #         if skew > SKEW_TOLERANCE:
    # Rotate the robot until it's not skewed. If skew positive,
    # the right is higher than the left, so the bot needs to turn
    # right to account for that, and vice versa.
    #             self.robot.drive_train.drive(skew * 0.2, abs(skew) / skew)
    #         else:
    # Right now this centering shit is jank af, let's just
    # do the auto-align shizz
    #             self.phase = 'skip-to-end'
    # self.phase = 'centering-x'

    #     elif self.phase == 'centering-x':
    # Now that we're looking straight on at the target, we can see
    # how off-center it is and basically move the robot to a position
    # such that is centered. First deal with the x-direction, since
    # y centering is trivial (just involves translating forwards and
    # backwards).
    #         off = GOAL_CENTER[x] - center[x]
    #         if off > CENTERING_X_TOLERANCE:
    #             if not super().isFinished():
    # The bot is in the process of finishing this stage.
    # We'll just wait...
    #                 return
    #             else:
    # Compute the scale factor to convert from 0-1 dimensions
    # to real world inch-by-inch dimensions.
    #                 scale = ACTUAL_GOAL_WIDTH_IN_INCHES / \
    #                     (top_right[x] - top_left[x])

    #                 distance_to_go = scale * (GOAL_CENTER[x] - center[x])
    #                 self.addSequential(auto_rotate.Rotate(90))
    #                 self.addSequential(auto_drive.Drive(distance_to_go))
    #                 self.addSequential(auto_rotate.Rotate(-90))
    #         else:
    #             self.phase = 'centering-y'

    #     elif self.phase == 'centering-y':
    # Center the y location. This is easier, since we can just look
    # in front of us the whole time and have an easy time.
    #         off = GOAL_CENTER[y] - center[y]
    #         if off > CENTERING_Y_TOLERANCE:
    #             self.robot.drive_train.drive(-off * 0.5, 0)
    #         else:
    #             self.is_aligned = True

    #     elif self.phase == 'skip-to-end':
    #         self.is_aligned = True

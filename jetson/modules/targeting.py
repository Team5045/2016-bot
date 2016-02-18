from __future__ import division
import math

import cv2
import numpy as np

import config

TAGRET_WIDTH_IN_INCHES = 20
FIELD_OF_VIEW_ANGLE = 34.25
TAN_FIELD_OF_VIEW_ANGLE = math.tan(math.radians(FIELD_OF_VIEW_ANGLE))


class Targeting(object):

    def __init__(self):
        self.settings = {
            'lower_hsv_bound': config.TARGETING_LOWER_HSV_BOUND,
            'upper_hsv_bound': config.TARGETING_UPPER_HSV_BOUND,
            'width': config.TARGETING_CAMERA_WIDTH,
            'height': config.TARGETING_CAMERA_HEIGHT,
            'fps': config.TARGETING_CAMERA_FPS,
            'white_balance': config.TARGETING_CAMERA_WHITE_BALANCE,
            'brightness': config.TARGETING_CAMERA_BRIGHTNESS,
            'exposure': config.TARGETING_CAMERA_EXPOSURE
        }

        self.last_frame = None  # For other modules to access

        self.cap = cv2.VideoCapture(config.TARGETING_CAMERA_PORT)
        self.cap.set(cv2.cv.CV_CAP_PROP_FPS, self.settings['fps'])
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.settings['width'])
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.settings['height'])
        self.cap.set(
            cv2.cv.CV_CAP_PROP_BRIGHTNESS, self.settings['brightness'])
        self.cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, self.settings['exposure'])
        # self.cap.set(cv2.cv.CV_CAP_PROP_WHITE_BALANCE,
        #              self.settings['white_balance'])

    def get_distance_from_target_of_width(self, width):
        return TAGRET_WIDTH_IN_INCHES * self.settings['width'] / \
            (2 * width * TAN_FIELD_OF_VIEW_ANGLE)

    def make_target_data(self, c):
        """c = Coords in the form:
        (c[0][0], c[0][1]) ---------- (c[1][0], c[1][1])
                |                             |
                |                             |
                |                             |
        (c[3][0], c[3][1]) ---------- (c[2][0], c[2][1])
        """
        full_width = self.settings['width']
        full_height = self.settings['height']
        x_center = full_width / 2
        y_center = full_height / 2

        distance = self.get_distance_from_target_of_width(c[2][0] - c[3][0])

        # Now convert coords to scaled [0, 1] coords, thus being
        # resolution-indendent. Also flip the y axis so top is positive,
        # bottom is negative, the giving coords in the form:
        # 1
        # |
        # |   * (x,y)
        # |
        # 0--------1
        scaled_coords = map(lambda (x, y):
                            (((x - x_center) + 1) / (2 * full_width),
                             (-(y - y_center) + 1) / (2 * full_height)),
                            c)

        return {
            'distance_away': distance,
            'coords': scaled_coords
        }

    def find_target(self):
        ret, frame = self.cap.read()
        self.last_frame = frame

        # Convert to HSV color space
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)  not needed??
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask to only include colors within bounds
        mask = cv2.inRange(hsv,
                           self.settings['lower_hsv_bound'],
                           self.settings['upper_hsv_bound'])

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        #  return self.make_target_data([[234,
        #  202], [51, 202], [51, 79], [234, 79]])

        if len(contours) > 0:
            # Find the largest contour
            cnt = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(cnt)

            if cv2.__version__.startswith('3'):
                box = cv2.boxPoints(rect)
            else:
                box = cv2.cv.boxPoints(rect)

            box = np.int0(box)
            return self.make_target_data(box)
        else:
            return False

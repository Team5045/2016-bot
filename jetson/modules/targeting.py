from __future__ import division
import math

import cv2
import numpy as np

from .sortpts_clockwise import sortpts_clockwise

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
        full_width = self.settings['width']
        full_height = self.settings['height']
        x_center = full_width / 2
        y_center = full_height / 2

        # Now convert coords to scaled [0, 1] coords, thus being
        # resolution-indendent. Resultant coords thus in the form:
        # 0
        # |
        # y   * (x, y)
        # |
        # 1
        #  0---x---1

        sorted_c = sortpts_clockwise(c)

        coords = map(lambda (x, y):
                     (round(((x - x_center) / (full_width)) + 0.5, 3),
                     round((y - y_center) / (full_height) + 0.5, 3)),
                     sorted_c)

        top_left = coords[0]
        top_right = coords[1]
        bottom_right = coords[2]
        bottom_left = coords[3]

        width = top_right[0] - top_left[0]
        if width > 0:
            distance = self.get_distance_from_target_of_width(width)
        else:
            distance = float('inf')

        return {
            'distance_away': distance,
            'coords': [
                top_left,
                top_right,
                bottom_right,
                bottom_left
            ]
        }

    def find_target(self):
        ret, frame = self.cap.read()

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask to only include colors within bounds
        mask = cv2.inRange(hsv,
                           self.settings['lower_hsv_bound'],
                           self.settings['upper_hsv_bound'])

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) > 0:
            # Find the largest contour
            cnt = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(cnt)

            if cv2.__version__.startswith('3'):
                box = cv2.boxPoints(rect)
            else:
                box = cv2.cv.boxPoints(rect)

            box = np.int0(box)

            # Draw box on frame for debugging/etc
            cv2.polylines(frame, [box], True, (255, 0, 0))

            result = self.make_target_data(box)
        else:
            result = False

        self.last_frame = frame
        return result

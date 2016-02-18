"""
vision.py
=========

Used to stream video and stuff.
"""

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import cv2
from PIL import Image

import config


class DriverVision(object):

    def __init__(self, targeting):
        self.settings = {
            'width': config.DRIVER_CAMERA_WIDTH,
            'height': config.DRIVER_CAMERA_HEIGHT,
            'fps': config.DRIVER_CAMERA_FPS,
            'brightness': config.DRIVER_CAMERA_BRIGHTNESS,
            'exposure': config.DRIVER_CAMERA_EXPOSURE
        }

        self.targeting = targeting

        self.cap = cv2.VideoCapture(config.DRIVER_CAMERA_PORT)
        self.cap.set(cv2.cv.CV_CAP_PROP_FPS, self.settings['fps'])
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.settings['width'])
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.settings['height'])
        self.cap.set(
            cv2.cv.CV_CAP_PROP_BRIGHTNESS, self.settings['brightness'])
        self.cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, self.settings['exposure'])

    def make_jpeg_from_frame(self, frame):
        """Converts an OpenCV frame to a JPEG buffer."""
        if frame is None or not frame.any():
            return 'none'

        image = Image.fromarray(frame)
        buf = StringIO()
        image.save(buf, 'JPEG')
        return buf.getvalue()

    def get_current_frame(self, camera='main', make_jpeg=True):
        """Fetches the current frame from the camera."""

        # Also publish targeting feed if selected
        if camera == 'shooting':
            frame = self.targeting.last_frame
        else:
            ret, frame = self.cap.read()

        if make_jpeg:
            return self.make_jpeg_from_frame(frame)
        else:
            return frame

import cv2


class CvPolyfill(object):
    """Strip the CV_ prefix"""
    def __getattribute__(self, attr):
        return object.__getattribute__(cv2, attr[3:])


def polyfill():
    if cv2.__version__.startswith('3'):
        cv2.cv = CvPolyfill()

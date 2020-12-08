import cv2

SETTING_WINDOW_RED = 'red hsv setting'
SETTING_WINDOW_BLUE = 'blue hsv setting'
SETTING_WINDOW = 'General'


interval = 100


def interval_change(interval_change):
    global interval
    if interval_change == 0:
        interval_change = 1
    interval = interval_change


def setup():
    cv2.namedWindow(SETTING_WINDOW)
    cv2.createTrackbar('interval', SETTING_WINDOW, 100, 100, interval_change)

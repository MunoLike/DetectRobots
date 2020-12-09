import cv2

SETTING_WINDOW_RED = 'red hsv setting'
SETTING_WINDOW_BLUE = 'blue hsv setting'
SETTING_WINDOW = 'General'

# default value
redh1_min = 0
redh1_max = 8
redh2_min = 242
redh2_max = 255
reds_min = 42
reds_max = 153
redv_min = 129
redv_max = 221

blueh_min = 105
blueh_max = 203
blues_min = 50
blues_max = 162
bluev_min = 89
bluev_max = 230


interval = 1


def interval_change(interval_change):
    global interval
    if interval_change == 0:
        interval_change = 1
    interval = interval_change


def setup():
    cv2.namedWindow(SETTING_WINDOW)
    cv2.createTrackbar('interval', SETTING_WINDOW, 100, 100, interval_change)

    # red
    def change_redh1_min(v):
        global redh1_min
        redh1_min = v

    def change_redh1_max(v):
        global redh1_max
        redh1_max = v

    def change_redh2_min(v):
        global redh2_min
        redh2_min = v

    def change_redh2_max(v):
        global redh2_max
        redh2_max = v

    def change_reds_min(v):
        global reds_min
        reds_min = v

    def change_reds_max(v):
        global reds_max
        reds_max = v

    def change_redv_min(v):
        global redv_min
        redv_min = v

    def change_redv_max(v):
        global redv_max
        redv_max = v

    cv2.namedWindow(SETTING_WINDOW_RED)
    cv2.createTrackbar('H1_min', SETTING_WINDOW_RED, 0, 255, change_redh1_min)
    cv2.createTrackbar('H1_max', SETTING_WINDOW_RED, 0, 255, change_redh1_max)
    cv2.createTrackbar('H2_min', SETTING_WINDOW_RED, 0, 255, change_redh2_min)
    cv2.createTrackbar('H2_max', SETTING_WINDOW_RED, 0, 255, change_redh2_max)
    cv2.createTrackbar('S_min', SETTING_WINDOW_RED, 0, 255, change_reds_min)
    cv2.createTrackbar('S_max', SETTING_WINDOW_RED, 0, 255, change_reds_max)
    cv2.createTrackbar('V_min', SETTING_WINDOW_RED, 0, 255, change_redv_min)
    cv2.createTrackbar('V_max', SETTING_WINDOW_RED, 0, 255, change_redv_max)

    # blue
    def change_blueh_min(v):
        global blueh_min
        blueh_min = v

    def change_blueh_max(v):
        global blueh_max
        blueh_max = v

    def change_blues_min(v):
        global blues_min
        blues_min = v

    def change_blues_max(v):
        global blues_max
        blues_max = v

    def change_bluev_min(v):
        global bluev_min
        bluev_min = v

    def change_bluev_max(v):
        global bluev_max
        bluev_max = v

    cv2.namedWindow(SETTING_WINDOW_BLUE)
    cv2.createTrackbar('H1', SETTING_WINDOW_BLUE, 0, 255, change_blueh_min)
    cv2.createTrackbar('H2', SETTING_WINDOW_BLUE, 0, 255, change_blueh_max)
    cv2.createTrackbar('S_min', SETTING_WINDOW_BLUE, 0, 255, change_blues_min)
    cv2.createTrackbar('S_max', SETTING_WINDOW_BLUE, 0, 255, change_blues_max)
    cv2.createTrackbar('V_min', SETTING_WINDOW_BLUE, 0, 255, change_bluev_min)
    cv2.createTrackbar('V_max', SETTING_WINDOW_BLUE, 0, 255, change_bluev_max)

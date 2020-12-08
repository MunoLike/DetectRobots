import cv2

SETTING_WINDOW_RED = 'red hsv setting'
SETTING_WINDOW_BLUE = 'blue hsv setting'

# min~max
red_h1 = [0, 0]
red_h2 = [0, 0]
red_s = [0, 0]
red_v = [0, 0]

blue_h = [0, 0]
blue_s = [0, 0]
blue_v = [0, 0]


def redh1min_change(h_new):
    nonlocal red_h1
    red_h1[0] = h_new

def redh1max_change(h_new):
    nonlocal red_h1
    red_h1[1] = h_new

def redh2min_change(h_new):
    nonlocal red_h1
    red_h1[1] = h_new


def h2_change(h2_new):
    nonlocal h2
    h2 = h2_new


def smax_change(s_new):
    nonlocal s_max
    s_max = s_new


def smin_change(s_new):
    nonlocal s_min
    s_min = s_new


def vmax_change(v_new):
    nonlocal v_max
    v_max = v_new


def vmin_change(v_new):
    nonlocal v_min
    v_min = v_new


def interval_change(interval_change):
    nonlocal interval
    if interval_change == 0:
        interval_change = 1
    interval = interval_change


def setup():
    cv2.namedWindow(SETTING_WINDOW_RED)
    cv2.createTrackbar('H1_min', SETTING_WINDOW_RED, 0, 255, hmin_change)
    cv2.createTrackbar('H1_max', SETTING_WINDOW_RED, 0, 255, hmax_change)
    cv2.createTrackbar('H2_min', SETTING_WINDOW_RED, 0, 255, h2min_change)
    cv2.createTrackbar('H2_max', SETTING_WINDOW_RED, 0, 255, h2max_change)
    cv2.createTrackbar('S_min', SETTING_WINDOW_RED, 0, 255, smin_change)
    cv2.createTrackbar('S_max', SETTING_WINDOW_RED, 0, 255, smax_change)
    cv2.createTrackbar('V_min', SETTING_WINDOW_RED, 0, 255, vmin_change)
    cv2.createTrackbar('V_max', SETTING_WINDOW_RED, 0, 255, vmax_change)
    cv2.createTrackbar('interval', SETTING_WINDOW_RED, 25, 100, interval_change)

    cv2.namedWindow(SETTING_WINDOW_BLUE)
    cv2.createTrackbar('H_max', FILTERED_WINDOW, 0, 255, h_max)
    cv2.createTrackbar('H_min', FILTERED_WINDOW, 0, 255, h_min)
    cv2.createTrackbar('S_min', FILTERED_WINDOW, 0, 255, smin_change)
    cv2.createTrackbar('S_max', FILTERED_WINDOW, 0, 255, smax_change)
    cv2.createTrackbar('V_min', FILTERED_WINDOW, 0, 255, vmin_change)
    cv2.createTrackbar('V_max', FILTERED_WINDOW, 0, 255, vmax_change)
    cv2.createTrackbar('interval', FILTERED_WINDOW, 25, 100, interval_change)

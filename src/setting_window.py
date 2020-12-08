import cv2

SETTING_WINDOW_RED = 'red hsv setting'
SETTING_WINDOW_BLUE = 'blue hsv setting'

def create_setting_window_red():
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


    
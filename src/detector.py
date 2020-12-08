import cv2
import numpy as np

# 光の乱れに弱い


def detect_red(hsv_f):
    h_min = 0
    h_max = 0
    h2_min = 0
    h2_max = 0
    s_max = 0
    s_min = 0
    v_max = 0
    v_min = 0

    # limit by color
    hsv_min = np.array([h_min, s_min, v_min])
    hsv_max = np.array([h_max, s_max, v_max])
    limited1 = cv2.inRange(hsv_f, hsv_min, hsv_max)

    hsv_min = np.array([h2_min, s_min, v_min])
    hsv_max = np.array([h2_max, s_max, v_max])
    limited2 = cv2.inRange(hsv_f, hsv_min, hsv_max)

    limited = limited1+limited2

    # Rinkaku
    contours, _ = cv2.findContours(limited, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    rect = None
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))

    if len(rects) > 1:
        rect = sorted(rects, key=lambda e: e[2]*e[3], reverse=True)[1]
    else:
        return [0, 0, 0, 0]

    return rect


def detect_blue(hsv_f):
    h_min = 0
    h_max = 0
    s_max = 0
    s_min = 0
    v_max = 0
    v_min = 0

    # limit by color
    hsv_min = np.array([h_min, s_min, v_min])
    hsv_max = np.array([h_max, s_max, v_max])
    limited = cv2.inRange(hsv_f, hsv_min, hsv_max)

    # get blue area
    contours, _ = cv2.findContours(limited, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    rect = None
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))

    if len(rects) > 1:
        rect = sorted(rects, key=lambda e: e[2]*e[3], reverse=True)[1]
    else:
        return [0, 0, 0, 0]

    return rect


# return position array [red, blue] = [[x,y],[x,y]](all float)
# frameSize: 正方形の画像がframeで入ってくることを想定している。その一辺の大きさをこれに入れる
def detect(frame, frameSize):

    hsv_f = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

    # opencv coordinates
    """[x,y,sizex,sizey]"""
    blue_p = detect_blue(hsv_f)
    red_p = detect_red(hsv_f)

    center_red = [0, 0]
    center_blue = [0, 0]

    # coordinate conversion
    center_blue[0] = blue_p[0] + blue_p[2]/2
    center_blue[1] = blue_p[1] + blue_p[3]/2

    center_red[0] = red_p[0] + red_p[2]/2  # calc center
    center_red[1] = red_p[1] + red_p[3]/2

    # opencv座標はyが反転しているため
    center_blue = [frameSize-center_blue[0], center_blue[1]]
    center_red = [frameSize-center_red[0], center_red[1]]

    # 6 means how many there are blocks in the field.
    block_unitSize = frameSize / 6

    normalized_bluep = [center_blue[0]/block_unitSize, center_blue[1]/block_unitSize]
    normalized_redp = [center_red[0]/block_unitSize, center_red[1]/block_unitSize]

    return (normalized_redp, normalized_bluep)

import cv2
import math
import numpy as np
import math

import setting_window as sw

# 光の乱れに弱い

DEBUG_HSV = True
DEBUG_POS = False
RED_WINDOW = 'red'
BLUE_WINDOW = 'blue'

LINE_COLOR = (3, 216, 255)
GRID_COLOR = (146, 182, 131)

# initial pos
position_red = [0.0, 0.0]
position_blue = [5.0, 5.0]


def debughsv(limited, circ, window_name):
    if DEBUG_HSV:
        bgr = cv2.cvtColor(limited, cv2.COLOR_GRAY2BGR)
        if not(circ is None):
            cv2.circle(bgr, (int(circ[0][0]), int(circ[0][1])), int(circ[1]), LINE_COLOR, 2)
            cv2.circle(bgr, (int(circ[0][0]), int(circ[0][1])), 3, LINE_COLOR, 3)
        print(f'{window_name}: ', circ[1]**2*math.pi)
        cv2.imshow(window_name, bgr)


def getLength(now, before):
    return math.sqrt((now[0]-before[0])**2+(now[1]-before[1])**2)


def getCircle(limited):
    # Rinkaku
    contours, _ = cv2.findContours(limited, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = []
    circ = None
    for contour in contours:
        approx = cv2.convexHull(contour)
        circ = cv2.minEnclosingCircle(approx)
        circles.append(np.array(circ))

    circ = max(circles, key=lambda e: e[1] ** 2 * math.pi, default=None)
    return circ


def detect_red(hsv_f):
    # limit by color
    hsv_min = np.array([sw.redh1_min, sw.reds_min, sw.redv_min])
    hsv_max = np.array([sw.redh1_max, sw.reds_max, sw.redv_max])
    limited1 = cv2.inRange(hsv_f, hsv_min, hsv_max)

    hsv_min = np.array([sw.redh2_min, sw.reds_min, sw.redv_min])
    hsv_max = np.array([sw.redh2_max, sw.reds_max, sw.redv_max])
    limited2 = cv2.inRange(hsv_f, hsv_min, hsv_max)

    limited = limited1+limited2

    # circlesが空＝円が見つからないとcircにはNoneが入る
    circ = getCircle(limited)

    debughsv(limited, circ, RED_WINDOW)

    if (circ is None):
        return None

    # 円の大きさチェック
    s = circ[1] ** 2 * math.pi
    if not(1000 < s and s < 2000):
        return None

    return circ


def detect_blue(hsv_f):
    # limit by color
    hsv_min = np.array([sw.blueh_min, sw.blues_min, sw.bluev_min])
    hsv_max = np.array([sw.blueh_max, sw.blues_max, sw.bluev_max])
    limited = cv2.inRange(hsv_f, hsv_min, hsv_max)

    # circlesが空＝円が見つからないとcircにはNoneが入る
    circ = getCircle(limited)

    debughsv(limited, circ, BLUE_WINDOW)

    if (circ is None):
        return None

    # 円の大きさチェック
    s = circ[1] ** 2 * math.pi
    if not(1000 < s and s < 2000):
        return None

    return circ


# return position array [red, blue] = [[x,y],[x,y]](all float)
# frameSize: 正方形の画像がframeで入ってくることを想定している。その一辺の大きさをこれに入れる
def detect(frame, frameSize):
    global position_blue
    global position_red

    hsv_f = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

    # opencv coordinates
    # error handling are low
    """((x,y),r)"""
    blue_p = detect_blue(hsv_f)
    red_p = detect_red(hsv_f)

    # Error Handling 1
    if (blue_p is None):
        return position_blue
    if red_p is None:
        return position_red

    center_red = [0, 0]
    center_blue = [0, 0]

    # coordinate conversion
    center_blue[0] = blue_p[0][0]
    center_blue[1] = blue_p[0][1]

    center_red[0] = red_p[0][0]
    center_red[1] = red_p[0][1]

    # opencv座標はyが反転しているため
    center_blue = [center_blue[0], frameSize-center_blue[1]]
    center_red = [center_red[0], frameSize-center_red[1]]

    # 6 means how many there are blocks in the field.
    block_unitSize = frameSize / 6

    normalized_bluep = [center_blue[0]/block_unitSize, center_blue[1]/block_unitSize]
    normalized_redp = [center_red[0]/block_unitSize, center_red[1]/block_unitSize]

    # Error Handling 2
    if 1.5 < getLength(normalized_bluep, position_blue):
        normalized_bluep = position_blue
    if 1.5 < getLength(normalized_redp, position_red):
        normalized_redp = position_red

    position_blue = normalized_bluep  # preserve
    position_red = normalized_redp

    if DEBUG_POS:
        block_height = int(frameSize/6)
        block_width = int(frameSize/6)

        for i in range(1, 6):
            frame = cv2.line(frame, (i*block_width, 0), (i*block_width, frameSize), GRID_COLOR, 3)
            frame = cv2.line(frame, (0, i*block_height), (frameSize, i*block_height), GRID_COLOR, 3)

        ###
        tmp_r = [int(f) for f in normalized_redp]
        tmp_b = [int(f) for f in normalized_bluep]
        print(tmp_r, tmp_b)
        ###

    return (normalized_redp, normalized_bluep)

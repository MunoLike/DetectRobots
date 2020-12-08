import cv2
import math
import numpy as np

# 光の乱れに弱い

DEBUG_HSV = True
DEBUG_POS = False
RED_WINDOW = 'red'
BLUE_WINDOW = 'blue'

LINE_COLOR = (3, 216, 255)
GRID_COLOR = (146, 182, 131)

position_red = [0.0, 0.0]
position_blue = [0.0, 0.0]


def lost_red():
    return ((0, 0), 0)


def lost_blue():
    return ((5, 5), 0)


def detect_red(hsv_f):
    h_min = 0
    h_max = 9
    h2_min = 0
    h2_max = 0
    s_min = 58
    s_max = 255
    v_min = 98
    v_max = 255

    # limit by color
    hsv_min = np.array([h_min, s_min, v_min])
    hsv_max = np.array([h_max, s_max, v_max])
    limited1 = cv2.inRange(hsv_f, hsv_min, hsv_max)

    hsv_min = np.array([h2_min, s_min, v_min])
    hsv_max = np.array([h2_max, s_max, v_max])
    limited2 = cv2.inRange(hsv_f, hsv_min, hsv_max)

    limited = limited1+limited2

    # Rinkaku
    contours, _ = cv2.findContours(limited, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = []
    circ = None
    for contour in contours:
        approx = cv2.convexHull(contour)
        circ = cv2.minEnclosingCircle(approx)
        circles.append(np.array(circ))

    if len(circles) > 1:
        circ = sorted(circles, key=lambda e: e[1] ** 2 * math.pi, reverse=True)[1]

        s = circ[1] ** 2 * math.pi
        if 1000 < s and s < 2000:
            return lost_red()

        if DEBUG_HSV:
            bgr = cv2.cvtColor(limited, cv2.COLOR_GRAY2BGR)
            cv2.circle(bgr, (int(circ[0][0]), int(circ[0][1])), int(circ[1]), LINE_COLOR, 2)
            cv2.circle(bgr, (int(circ[0][0]), int(circ[0][1])), 3, LINE_COLOR, 3)
            print('red: ', circ[1]**2*math.pi)
            cv2.imshow(RED_WINDOW, bgr)

    else:
        return lost_red()

    return circ


def detect_blue(hsv_f):
    h_min = 114
    h_max = 200
    s_min = 70
    s_max = 255
    v_min = 91
    v_max = 255

    # limit by color
    hsv_min = np.array([h_min, s_min, v_min])
    hsv_max = np.array([h_max, s_max, v_max])
    limited = cv2.inRange(hsv_f, hsv_min, hsv_max)

    # Rinkaku
    contours, _ = cv2.findContours(limited, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = []
    circ = None
    for contour in contours:
        approx = cv2.convexHull(contour)
        circ = cv2.minEnclosingCircle(approx)
        circles.append(np.array(circ))

    if len(circles) > 1:
        circ = sorted(circles, key=lambda e: e[1] ** 2 * math.pi, reverse=True)[1]

        s = circ[1] ** 2 * math.pi
        if 1000 < s and s < 2000:
            return lost_red()

        if DEBUG_HSV:
            bgr = cv2.cvtColor(limited, cv2.COLOR_GRAY2BGR)
            cv2.circle(bgr, (int(circ[0][0]), int(circ[0][1])), int(circ[1]), LINE_COLOR, 2)
            cv2.circle(bgr, (int(circ[0][0]), int(circ[0][1])), 3, LINE_COLOR, 3)
            print('blue: ', circ[1]**2*math.pi)
            cv2.imshow(BLUE_WINDOW, bgr)

    else:
        # 見失った
        return lost_blue()

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

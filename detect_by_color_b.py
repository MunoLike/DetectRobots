import cv2
import numpy as np

# BGR
LINE_COLOR = (3, 216, 255)
HSV_WINDOW = 'hsv'
FILTERED_WINDOW = 'filtered'

hsv = None

# profile_2: h:141~185, s:75~255, v:91~255
#


def mouseCallback(e, x, y, flags, img):
    if e == cv2.EVENT_LBUTTONDBLCLK:
        print(hsv[y, x])


def main():
    global hsv

    h = 0
    h2 = 0
    s_max = 0
    s_min = 0
    v_max = 0
    v_min = 0
    interval = 25

    FILTER = 2
    cap = cv2.VideoCapture(r'./camvids/5.mp4')

    cap.set(cv2.CAP_PROP_FPS, 30)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # define HSV Fi
    def h_change(h_new):
        nonlocal h
        h = h_new

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

    cv2.namedWindow(FILTERED_WINDOW, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('H1', FILTERED_WINDOW, 0, 255, h_change)
    cv2.createTrackbar('H2', FILTERED_WINDOW, 0, 255, h2_change)
    cv2.createTrackbar('S_min', FILTERED_WINDOW, 0, 255, smin_change)
    cv2.createTrackbar('S_max', FILTERED_WINDOW, 0, 255, smax_change)
    cv2.createTrackbar('V_min', FILTERED_WINDOW, 0, 255, vmin_change)
    cv2.createTrackbar('V_max', FILTERED_WINDOW, 0, 255, vmax_change)
    cv2.createTrackbar('interval', FILTERED_WINDOW, 25, 100, interval_change)

    while True:
        success, img = cap.read()
        if not(success):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ループ再生
            continue

        img = cv2.resize(img, (320, 240))

        cv2.imshow('Video', img)

        # filter
        filtered = None
        if FILTER == 0:
            filtered = cv2.GaussianBlur(img, (7, 7), 0)
        elif FILTER == 1:
            filtered = cv2.bilateralFilter(img, 10, 100, 100)
        elif FILTER == 2:
            filtered = img

        # convert into hsv
        hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV_FULL)
        cv2.imshow(HSV_WINDOW, hsv)
        cv2.setMouseCallback(HSV_WINDOW, mouseCallback)

        # limit by color
        hsv_min = np.array([h, s_min, v_min])
        hsv_max = np.array([h2, s_max, v_max])
        limited1 = cv2.inRange(hsv, hsv_min, hsv_max)

        limited = limited1

        # Rinkaku
        contours, _ = cv2.findContours(limited, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects.append(np.array(rect))

        # render a rectangle
        limited = cv2.cvtColor(limited, cv2.COLOR_GRAY2BGR)
        if len(rects) > 1:
            # 今は2番目に面積の大きいものを取得しているが、実機が走り回るとどうだろうか
            # スタート地点と被ったときの条件分岐を考える必要がある
            rect = sorted(rects, key=lambda e: e[2]*e[3], reverse=True)[1]
            cv2.rectangle(limited, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), LINE_COLOR, 1)
            cv2.circle(limited, tuple(rect[0:2]+rect[2:4]//2), 3, LINE_COLOR, 3)

        #
        cv2.imshow(FILTERED_WINDOW, limited)

        if cv2.waitKey(interval) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

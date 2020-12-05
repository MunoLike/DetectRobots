import cv2
import numpy as np

# BGR
LINE_COLOR = (3, 216, 255)
HSV_WINDOW = 'hsv'
FILTERED_WINDOW = 'filtered'

hsv = None

# 赤色のおすすめパラメータはh1=0~19,h2=228~255,s=103~255,v=125~255


def mouseCallback(e, x, y, flags, img):
    if e == cv2.EVENT_LBUTTONDBLCLK:
        print(hsv[y, x])


def main():
    global hsv

    h_min = 0
    h_max = 0
    h2_min = 0
    h2_max = 0
    s = 0
    v = 0

    FILTER = 2
    cap = cv2.VideoCapture(r'./camvids/2.mp4')

    cap.set(cv2.CAP_PROP_FPS, 30)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # define HSV Fi
    def hmin_change(h_new):
        nonlocal h_min
        h_min = h_new

    def hmax_change(h_new):
        nonlocal h_max
        h_max = h_new

    def h2min_change(h2_new):
        nonlocal h2_min
        h2_min = h2_new

    def h2max_change(h2_new):
        nonlocal h2_max
        h2_max = h2_new

    def s_change(s_new):
        nonlocal s
        s = s_new

    def v_change(v_new):
        nonlocal v
        v = v_new

    cv2.namedWindow(FILTERED_WINDOW)
    cv2.createTrackbar('H1_min', FILTERED_WINDOW, 0, 255, hmin_change)
    cv2.createTrackbar('H1_max', FILTERED_WINDOW, 0, 255, hmax_change)
    cv2.createTrackbar('H2_min', FILTERED_WINDOW, 0, 255, h2min_change)
    cv2.createTrackbar('H2_max', FILTERED_WINDOW, 0, 255, h2max_change)
    cv2.createTrackbar('S', FILTERED_WINDOW, 0, 255, s_change)
    cv2.createTrackbar('V', FILTERED_WINDOW, 0, 255, v_change)

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
        hsv_min = np.array([h_min, s, v])
        hsv_max = np.array([h_max, 255, 255])
        limited1 = cv2.inRange(hsv, hsv_min, hsv_max)

        hsv_min = np.array([h2_min, s, v])
        hsv_max = np.array([h2_max, 255, 255])
        limited2 = cv2.inRange(hsv, hsv_min, hsv_max)

        limited = limited1+limited2

        # Rinkaku
        contours, _ = cv2.findContours(limited, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects.append(np.array(rect))

        # render a rectangle
        limited = cv2.cvtColor(limited, cv2.COLOR_GRAY2BGR)
        if len(rects) > 0:
            # 今は2番目に面積の大きいものを取得しているが、実機が走り回るとどうだろうか
            # スタート地点と被ったときの条件分岐を考える必要がある
            rect = sorted(rects, key=lambda e: e[2]*e[3], reverse=True)[1]
            #rect = max(rects, key=(lambda x: x[2]*x[3]))
            cv2.rectangle(limited, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), LINE_COLOR, 3)

        #
        cv2.imshow(FILTERED_WINDOW, limited)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

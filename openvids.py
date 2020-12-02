import cv2
import numpy as np

HSV_WINDOW = 'hsv'
FILTERED_WINDOW = 'filtered'

hsv = None


def mouseCallback(e, x, y, flags, img):
    if e == cv2.EVENT_LBUTTONDBLCLK:
        print(hsv[y, x])


def main():
    global hsv

    h = 0
    s = 0
    v = 0

    FILTER = 2
    cap = cv2.VideoCapture(r'./camvids/1.mp4')

    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # define HSV Fi
    def h_change(h_new):
        nonlocal h
        h = h_new

    def s_change(s_new):
        nonlocal s
        s = s_new

    def v_change(v_new):
        nonlocal v
        v = v_new

    cv2.namedWindow(FILTERED_WINDOW)
    cv2.createTrackbar('H', FILTERED_WINDOW, 0, 179, h_change)
    cv2.createTrackbar('S', FILTERED_WINDOW, 0, 255, s_change)
    cv2.createTrackbar('V', FILTERED_WINDOW, 0, 255, v_change)

    while True:
        success, img = cap.read()
        if not(success):
            break

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
        hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
        cv2.imshow(HSV_WINDOW, hsv)
        cv2.setMouseCallback(HSV_WINDOW, mouseCallback)

        # limit by color
        hsv_min = np.array([h, s, v])
        hsv_max = np.array([179, 255, 255])
        limited = cv2.inRange(hsv, hsv_min, hsv_max)

        # umeume
        kernel = np.ones((5, 5), np.uint8)
        hsv_vec = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel)

        cv2.imshow(FILTERED_WINDOW, limited)

    # TODO:赤だけ抜く。色相'環'は円径だからHは0~30と300~360あたり
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

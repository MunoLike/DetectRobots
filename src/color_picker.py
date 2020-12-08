import cv2

COLOR_PICKER_WINDOW = 'color picker'

hsv = None


def color_picker(e, x, y, flags, _):
    if e == cv2.EVENT_LBUTTONDOWN:
        print(hsv[y, x])


def setup():
    cv2.namedWindow(COLOR_PICKER_WINDOW, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(COLOR_PICKER_WINDOW, color_picker)


def event_loop(frame):
    global hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

    cv2.imshow(COLOR_PICKER_WINDOW, frame)

import cv2
import numpy as np
import frame_transformer as ft
import perspective_transformer as pt
import detector as dt
import setting_window as sw
import color_picker as cp

# set value 0 for using camera
cap = cv2.VideoCapture(r'./camvids/2.mp4')

# frame size
(WIDTH, HEIGHT) = (640, 480)

#
VIEW_WINDOW = 'view'

#
ADJUST_COLOR_WINDOW = False


def main():
    pt.setup()

    if ADJUST_COLOR_WINDOW:
        cp.setup()
        sw.setup()

    while True:
        if cv2.waitKey(sw.interval) == ord('q'):
            break

        success, frame = cap.read()
        if not(success):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ループ再生
            continue

        frame = pt.event_loop(frame, HEIGHT, WIDTH)
        if frame is None:
            continue

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.bilateralFilter(frame, 10, 100, 100)

        if ADJUST_COLOR_WINDOW:
            cp.event_loop(frame)

        # redp, bluep
        coords = dt.detect(frame, WIDTH)

        print('redp:', list(map(int, coords[0])), 'bluep:', list(map(int, coords[1])))

        cv2.imshow(VIEW_WINDOW, frame)


if __name__ == "__main__":
    main()

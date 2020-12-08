import cv2
import numpy as np
import frame_transformer as ft
import perspective_transformer as pt
import detector as dt
import setting_window as sw

# set value 0 for using camera
cap = cv2.VideoCapture(r'./camvids/4.mp4')

# frame size
(WIDTH, HEIGHT) = (640, 480)

#
RESULT_WINDOW = 'result'


def main():
    pt.setup()
    sw.setup()

    while True:
        if cv2.waitKey(sw.interval) == ord('q'):
            break

        success, frame = cap.read()
        if not(success):
            break

        frame = pt.event_loop(frame, HEIGHT, WIDTH)
        if frame is None:
            continue

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame = cv2.bilateralFilter(frame, 10, 100, 100)
        coords = dt.detect(frame, WIDTH)


if __name__ == "__main__":
    main()

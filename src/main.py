import cv2
import numpy as np
import frame_transformer as ft
import perspective_transformer as pt
import detector as dt
import setting_window as sw

# set value 0 for using camera
cap = cv2.VideoCapture(r'./camvids/1.mp4')

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

        p_frame = pt.event_loop(frame, HEIGHT, WIDTH)
        if p_frame is None:
            continue

        filtered_frame = cv2.bilateralFilter(p_frame, 10, 100, 100)
        coords = dt.detect(filtered_frame, WIDTH)

        cv2.imshow(RESULT_WINDOW, filtered_frame)


if __name__ == "__main__":
    main()

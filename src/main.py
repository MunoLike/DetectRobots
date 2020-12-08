import cv2
import numpy as np
import frame_transformer as ft
import perspective_transformer as pt
import detector as dt

# set value 0 for using camera
cap = cv2.VideoCapture(r'./camvids/4.mp4')

# frame size
(WIDTH, HEIGHT) = (640, 480)

#
RESULT_WINDOW = 'result'


def main():
    pt.setup()

    while True:
        if cv2.waitKey(100) == ord('q'):
            break

        success, frame = cap.read()
        if not(success):
            break

        p_frame = pt.event_loop(frame, HEIGHT, WIDTH)
        if p_frame is None:
            continue

        r_frame = cv2.rotate(p_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        filtered_frame = cv2.bilateralFilter(r_frame, 10, 100, 100)

        coords = dt.detect(filtered_frame, WIDTH)

        cv2.imshow(RESULT_WINDOW, filtered_frame)


if __name__ == "__main__":
    main()

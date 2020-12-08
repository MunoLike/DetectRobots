import cv2
import numpy as np
import frame_transformer as ft
import perspective_transformer as pt

# set value 0 for using camera
cap = cv2.VideoCapture(r'./camvids/2.mp4')

# frame size
(WIDTH, HEIGHT) = (640, 480)

#
RESULT_WINDOW = 'result'


def main():
    pt.setup()

    while True:
        success, frame = cap.read()
        if not(success):
            break

        p_frame = pt.event_loop(frame, WIDTH, HEIGHT)
        if p_frame is None:
            continue

        cv2.imshow(RESULT_WINDOW, frame)
        if cv2.waitKey(100) == ord('q'):
            break


if __name__ == "__main__":
    main()

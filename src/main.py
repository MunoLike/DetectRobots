import cv2
import numpy as np
import logging
import frame_transformer as ft
import perspective_transformer as pt
import detector as dt
import setting_window as sw
import color_picker as cp
import server
import variables

import threading

# set value 0 for using camera
# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture(r'./camvids/2.mp4')

# frame size
(WIDTH, HEIGHT) = (320, 240)

#
VIEW_WINDOW = 'view'

#
ADJUST_WINDOW = True
DEBUG_PRINTCOORD = False


def main():
    lock = threading.RLock()

    # start server
    server_thread = threading.Thread(target=server.server, args=(lock,))
    server_thread.setDaemon(True)
    server_thread.start()

    if ADJUST_WINDOW:
        pt.setup()
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

        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.medianBlur(frame, 7)

        if ADJUST_WINDOW:
            cp.event_loop(frame)

        # redp, bluep
        tmp = dt.detect(frame, WIDTH)

        # lock
        lock.acquire()
        variables.coords = tmp
        lock.release()

        if DEBUG_PRINTCOORD:
            def f(e): return '{:.3g}'.format(e)
            print('redp:', list(map(f, variables.coords[0])), 'bluep:', list(map(f, variables.coords[1])))

        cv2.imshow(VIEW_WINDOW, frame)


if __name__ == "__main__":
    main()

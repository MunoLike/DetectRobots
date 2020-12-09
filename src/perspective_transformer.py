import cv2
import numpy as np
import logging
import frame_transformer as ft
import main

# Window names
SQR_WINDOW = 'square editor'

# before/after transforming points
src_pt = np.array([
    [174, 143],
    [164, 697],
    [502, 725],
    [488, 105]
], dtype=np.float32)
dst_pt = np.zeros((4, 2), dtype=np.float32)

# check how times the window is clicked
click_cnt = 0

# square editing screen's margin size
MARGIN = 100

#
h_mat = None
editable_frame = None

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def recordClick(e, x, y, flags, _):
    global src_pt
    global click_cnt
    if e == cv2.EVENT_LBUTTONDBLCLK:
        logger.info(f'{x}, {y}')
        src_pt[click_cnt] = [x, y]
        click_cnt += 1


def setup():
    cv2.namedWindow(SQR_WINDOW, cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback(SQR_WINDOW, recordClick)


def event_loop(frame, HEIGHT, WIDTH):
    global click_cnt
    global h_mat
    global editable_frame
    global src_pt
    global dst_pt

    frame = cv2.resize(frame, (HEIGHT, WIDTH))
    pil_img = ft.cv2pil(frame)
    pil_img = ft.add_margin(pil_img, MARGIN, MARGIN, MARGIN, MARGIN, (255, 255, 255))
    frame = ft.pil2cv(pil_img)
    editable_frame = frame.copy()

    #
    for i in range(click_cnt):
        cv2.circle(editable_frame, tuple(src_pt[i]), 5, (0, 255, 0), -1)
    #
    if click_cnt > 3:
        click_cnt = 0
        editable_frame = frame.copy()  # reset Image

    (w_orig, w_end) = (0, WIDTH)
    (h_orig, h_end) = (0, WIDTH)

    dst_pt[0] = [w_orig, h_orig]
    dst_pt[1] = [w_orig, h_end]
    dst_pt[2] = [w_end, h_end]
    dst_pt[3] = [w_end, h_orig]

    h_mat = cv2.getPerspectiveTransform(src_pt, dst_pt)

    #
    if main.ADJUST_WINDOW:
        cv2.imshow(SQR_WINDOW, editable_frame)

    # 点がない時をはじく
    if (h_mat is None):
        return None

    result = cv2.warpPerspective(frame, h_mat, (WIDTH, WIDTH))
    return result

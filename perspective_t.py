import cv2
import numpy as np

WIDTH = 640
HEIGHT = 480
IMG_WINDOW = 'img'
RESULT_WINDOW='result'

src_pt = np.zeros((4, 2), dtype=np.float32)
dst_pt = np.zeros((4, 2), dtype=np.float32)
img = None
editable_img = None

click_cnt = 0


def mouseCallback(e, x, y, flags, _):
    global src_pt
    global click_cnt
    if e == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        src_pt[click_cnt] = [x, y]
        click_cnt += 1
 


def main():
    global img
    global editable_img
    global src_pt
    global dst_pt
    global click_cnt

    result = None


    img = cv2.imread('camvids/pic1.jpg')
    img = cv2.resize(img, (WIDTH, HEIGHT))
    editable_img = img.copy()
    cv2.namedWindow(IMG_WINDOW)
    cv2.namedWindow(RESULT_WINDOW)
    cv2.setMouseCallback(IMG_WINDOW, mouseCallback)

    while True:
        if click_cnt > 3:
            click_cnt = 0
            dst_pt[0] = [src_pt[0][0], src_pt[3][1]]
            dst_pt[1] = [src_pt[0][0], src_pt[2][1]]
            dst_pt[2] = [src_pt[3][0], src_pt[2][1]]
            dst_pt[3] = src_pt[3]

            h_mat = cv2.getPerspectiveTransform(src_pt, dst_pt)
            result = cv2.warpPerspective(editable_img, h_mat, (HEIGHT+100,WIDTH+100))
            cv2.imshow(RESULT_WINDOW, result)

        #
        for i in range(click_cnt):
            cv2.circle(img, tuple(src_pt[i]), 10, (0,255,0), -1)


        cv2.imshow(IMG_WINDOW, img)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()

import cv2
import numpy as np

IMG_WINDOW='img'
src_pt = np.float32([[0]*4 for i in range(4)])
dst_pt = np.float32([[0]*4 for i in range(4)])
img = None

def mouseCallback(e, x, y, flags, _):
    if e == cv2.EVENT_LBUTTONDBLCLK:
        print(img[y,x])


def main():
    global img
    global src_pt
    global dst_pt

    img = cv2.imread('camvids/pic1.jpg')
    cv2.imshow(IMG_WINDOW, img)
    cv2.setMouseCallback(IMG_WINDOW, mouseCallback)

    while True:
        if cv2.waitKey(0):
            break
    

if __name__ == '__main__':
    main()
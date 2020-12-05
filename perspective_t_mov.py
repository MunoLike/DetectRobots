import cv2
from PIL import Image
import numpy as np

WIDTH = 640
HEIGHT = 480
MARGIN = 100
IMG_WINDOW = 'img'
RESULT_WINDOW = 'result'
TRIMMED_WINDOW = 'trimmed'

src_pt = np.zeros((4, 2), dtype=np.float32)
dst_pt = np.zeros((4, 2), dtype=np.float32)
img = None
editable_img = None

click_cnt = 0


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def recordClick(e, x, y, flags, _):
    global src_pt
    global click_cnt
    if e == cv2.EVENT_LBUTTONDBLCLK:
        src_pt[click_cnt] = [x, y]
        click_cnt += 1


def mdbg(e, x, y, flags, _):
    if e == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


def main():
    global img
    global editable_img
    global src_pt
    global dst_pt
    global click_cnt

    h_mat = None
    result = None

    cap = cv2.VideoCapture(r'./camvids/2.mp4')


    cv2.namedWindow(IMG_WINDOW)
    cv2.namedWindow(RESULT_WINDOW, cv2.WINDOW_NORMAL)

    cv2.setMouseCallback(IMG_WINDOW, recordClick)

    while True:
        success, img = cap.read()
        if not(success):
            break

        img = cv2.resize(img, (WIDTH, HEIGHT))

        pil_img = cv2pil(img)
        pil_img = add_margin(pil_img, MARGIN, MARGIN, MARGIN, MARGIN, (255, 255, 255))
        img = pil2cv(pil_img)

        editable_img = img.copy()


        for i in range(click_cnt):
            cv2.circle(editable_img, tuple(src_pt[i]), 5, (0, 255, 0), -1)

        #
        if click_cnt > 3:
            click_cnt = 0

            (w_orig, w_end) = (0,WIDTH)
            (h_orig, h_end) = (0,WIDTH)

            dst_pt[0] = [w_orig, h_orig]
            dst_pt[1] = [w_orig, h_end]
            dst_pt[2] = [w_end, h_end]
            dst_pt[3] = [w_end, h_orig]

            h_mat = cv2.getPerspectiveTransform(src_pt, dst_pt)
            editable_img = img.copy()  # reset Image

        if not(h_mat is None):
            result = cv2.warpPerspective(img, h_mat, (WIDTH, WIDTH))
            cv2.imshow(RESULT_WINDOW, result)

        #

        cv2.imshow(IMG_WINDOW, editable_img)
        if cv2.waitKey(100) == ord('q'):
            break


if __name__ == '__main__':
    main()

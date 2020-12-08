import cv2

GRIDDED_WINDOW = 'grid'

# arranged: BGR
LINE_COLOR = (146, 182, 131)


def main():
    img = cv2.imread('camvids/transformed.png')
    HEIGHT, WIDTH = img.shape[:2]

    cv2.namedWindow(GRIDDED_WINDOW)

    block_height = int(HEIGHT/6)
    block_width = int(WIDTH/6)

    for i in range(1, 6):
        cv2.line(img, (i*block_width, 0), (i*block_width, HEIGHT), LINE_COLOR, 3)
        cv2.line(img, (0, i*block_height), (WIDTH, i*block_height), LINE_COLOR, 3)

    cv2.imshow(GRIDDED_WINDOW, img)
    while cv2.waitKey(0) != ord('q'):
        break


if __name__ == "__main__":
    main()

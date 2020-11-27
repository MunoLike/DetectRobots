import cv2

FILTER = 1

print(cv2.cuda.getCudaEnabledDeviceCount())

cap = cv2.VideoCapture(r'./camvids/1.mp4')
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    success, img = cap.read()
    if not(success):
        break

    img = cv2.resize(img, (320, 240))

    cv2.imshow('Video', img)

    filtered = None
    if FILTER == 0:
        filtered = cv2.GaussianBlur(img, (7, 7), 0)
        cv2.imshow('Gaus', filtered)
    elif FILTER == 1:
        filtered = cv2.bilateralFilter(img, 10, 100, 100)
        cv2.imshow('Bilateral', filtered)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera tidak ditemukan")
    exit()

print("Camera berhasil dibuka")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Camera Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key in (ord("q"), ord("Q"), 27):
        break

cap.release()

cv2.destroyAllWindows()
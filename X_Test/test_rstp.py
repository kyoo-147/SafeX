# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import cv2
import dlib

# Sử dụng máy dò khuôn mặt HOG có hỗ trợ CUDA
detector = dlib.get_frontal_face_detector()
# Đọc video từ camera hoặc luồng RTSP
cap = cv2.VideoCapture("rtsp://admin:MRRZHJ@192.168.1.2:554/H.264")
buffer_size = 10  # Số lượng khung hình trong bộ đệm

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()
# Tăng kích thước bộ đệm
cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break
    # Resize khung hình xuống 640x480
    frame = cv2.resize(frame, (640, 480))
    # Chuyển đổi khung hình sang định dạng grayscale để xử lý nhanh hơn
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Phát hiện khuôn mặt
    faces = detector(gray, 1)
    for face in faces:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

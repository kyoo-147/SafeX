# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import cv2
import numpy as np

# Mở webcam và ảnh
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("rtsp://admin:MRRZHJ@192.168.1.2:554/H.264")
img = cv2.imread('X_UI/Layout_Recog.png')  # Thay đổi đường dẫn đến ảnh của bạn

while True:
    # Đọc khung hình từ webcam
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    # Kiểm tra xem có đọc được khung hình hay không
    if not ret:
        print("Không thể đọc được khung hình!")
        break
    # Chuyển đổi kích thước ảnh cho phù hợp với khung hình
    img_resized = cv2.resize(img, (frame.shape[1], frame.shape[0]))
    # Chuyển đổi ảnh thành hệ màu BGR
    img_resized_BGR = cv2.cvtColor(img_resized, cv2.COLOR_BGRA2BGR)
    # Tạo mask để che các phần không cần thiết của ảnh
    mask = cv2.inRange(img_resized_BGR, np.array([0, 0, 0]), np.array([255, 255, 255]))
    # Hợp nhất ảnh và khung hình
    overlay = cv2.addWeighted(frame, 1, img_resized_BGR, 0.5, 0)
    final_frame = cv2.bitwise_and(overlay, overlay, mask=mask)
    # Hiển thị khung hình cuối cùng
    cv2.imshow('Webcam', final_frame)
    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng nguồn tài nguyên
cap.release()
cv2.destroyAllWindows()

# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import cv2
import logging

logging.basicConfig(level=logging.DEBUG)

class FaceRecognizer:
    def __init__(self):
        self.frame_cnt = 0

    def process(self, stream):
        while stream.isOpened():
            self.frame_cnt += 1
            logging.debug("Frame %d starts", self.frame_cnt)
            flag, img_rd = stream.read()
            if not flag or img_rd is None:
                logging.error("Failed to read frame %d", self.frame_cnt)
                continue
            try:
                new_width = 640
                new_height = 480
                img_rd = cv2.resize(img_rd, (new_width, new_height))
            except cv2.error as e:
                logging.error("OpenCV error during resizing frame %d: %s", self.frame_cnt, e)
                continue
            # Hiển thị khung hình
            cv2.imshow("camera", img_rd)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            logging.debug("Frame ends\n\n")

    def run(self):
        rtsp_url = "rtsp://admin:MRRZHJ@192.168.1.2:554/H.264"
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            logging.error("Failed to open RTSP stream directly.")
            return
        self.process(cap)
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Face_Recognizer_con = FaceRecognizer()
    Face_Recognizer_con.run()

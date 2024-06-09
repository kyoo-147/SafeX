# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
# Import library
import dlib
import numpy as np
import cv2
import os
import pandas as pd
import time
import logging
# from X_Alert import X_Buzzer_Alarm
import uuid
from X_Utils.X_Database import initialize_sheet, log_to_google_sheets
from X_Utils.X_Email_Multi import known_send_email, unknown_send_email
from datetime import datetime

# Get model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('X_Center_Model/Model_Dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("X_Center_Model/Model_Dlib/dlib_face_recognition_resnet_model_v1.dat")

# Main process
class Face_Recognizer:
    def __init__(self):
        self.font = cv2.FONT_ITALIC
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()
        self.frame_cnt = 0
        self.face_features_known_list = []
        self.face_name_known_list = []
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []
        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []
        self.last_frame_face_cnt = 0 
        self.current_frame_face_cnt = 0
        self.current_frame_face_X_e_distance_list = []
        self.current_frame_face_position_list = []
        self.current_frame_face_feature_list = []
        self.last_current_frame_centroid_e_distance = 0
        self.reclassify_interval_cnt = 0
        self.reclassify_interval = 10
        self.last_alert_time = time.time() 
        self.unknown_start_time = None  # Thời điểm bắt đầu phát hiện "unknown"
        self.unknown_detected = False  # Trạng thái phát hiện "unknown"
        self.alarm_triggered_1 = False  # Trạng thái cảnh báo lần 1
        self.alarm_triggered_2 = False  # Trạng thái cảnh báo lần 2
        
        # Khởi tạo các ngưỡng thời gian kích hoạt cảnh báo
        self.threshold_time_1 = 5  # Ngưỡng thời gian cho cảnh báo lần 1 (giây)
        self.threshold_time_2 = 10  # Ngưỡng thời gian cho cảnh báo lần 2 (giây)
        
    # Get data face landmark from csv file training
    def get_face_database(self):
        if os.path.exists("X_Center_Data/features_all.csv"):
            path_features_known_csv = "X_Center_Data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                for j in range(1, 129):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            logging.info("Faces in Database： %d", len(self.face_features_known_list))
            return 1
        else:
            logging.warning("Cannot find model data file 'features_all.csv'!")
            logging.warning("Please register your user data information' "
                            "and training data to perform system monitoring operations")
            return 0
        
    # FPS
    def update_fps(self):
        now = time.time()
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now
    
    # Cal e distance    
    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1-feature_2)))
        return dist
    
    # Cal centroid track
    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                    self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])
                e_distance_current_frame_person_x_list.append(
                    self.last_current_frame_centroid_e_distance)
            last_frame_num = e_distance_current_frame_person_x_list.index(
                min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]
            
    def draw_note(self, img_rd):
        cv2.putText(img_rd, "SafeX | Face Recognition Tracking", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:    " + str(self.fps.__round__(2)), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Face:  " + str(self.current_frame_face_cnt), (20, 130), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Exit", (20, 420), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
                
    # support process
    def process(self, stream):
        if self.get_face_database():
            while stream.isOpened():
                self.frame_cnt += 1
                logging.debug("Frame " + str(self.frame_cnt) + " starts")
                flag, img_rd = stream.read()
                
                # Resize to default frame if you need
                
                # if not flag or img_rd is None:
                #     logging.error("Failed to read frame %d", self.frame_cnt)
                #     continue
                # try:
                #     new_width = 640
                #     new_height = 480
                #     img_rd = cv2.resize(img_rd, (new_width, new_height))
                # except cv2.error as e:
                #     logging.error("OpenCV error during resizing frame %d: %s", self.frame_cnt, e)
                #     continue
                
                kk = cv2.waitKey(1) 
                faces = detector(img_rd, 0)
                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)
                self.last_frame_face_name_list = self.current_frame_face_name_list[:]
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []
                
                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                        self.reclassify_interval_cnt != self.reclassify_interval):
                    logging.debug("scene 1: No face cnt changes in this frame!")
                    self.current_frame_face_position_list = []
                    
                    if "unknown" in self.current_frame_face_name_list:
                        logging.debug("  There are unknown faces, let's start counting reclassify_interval_cnt")
                        self.reclassify_interval_cnt += 1
                        if not self.unknown_detected:
                            # Bắt đầu đếm thời gian nếu "unknown" được phát hiện lần đầu
                            self.unknown_start_time = time.time()
                            self.unknown_detected = True
                            self.alarm_triggered_1 = False  # Reset cảnh báo lần 1
                            self.alarm_triggered_2 = False  # Reset cảnh báo lần 2
                        else:
                            # Kiểm tra thời gian từ khi phát hiện "unknown"
                            current_time = time.time()
                            time_since_unknown_detected = current_time - self.unknown_start_time

                            #TODO: Kích hoạt còi báo
                            if time_since_unknown_detected >= self.threshold_time_2 and not self.alarm_triggered_2:
                                # Phát còi lần 2 (2 lần)
                                # self.X_Buzzer_Alarm(40, 1, 1, 5)
                                self.alarm_triggered_2 = True
                                print("Warning: Unknown detected for 10 seconds (2 alarms)")
                            elif time_since_unknown_detected >= self.threshold_time_1 and not self.alarm_triggered_1:
                                # Phát còi lần 1 (1 lần)
                                # self.X_Buzzer_Alarm(40, 1, 1, 5)
                                self.alarm_triggered_1 = True
                                print("Warning: Unknown detected for 5 seconds (1 alarm)")
                    else:
                        self.unknown_start_time = None
                        self.unknown_detected = False
                        self.alarm_triggered_1 = False
                        self.alarm_triggered_2 = False                       
                        
                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])
                            left, top, right, bottom = d.left(), d.top(), d.right(), d.bottom()
                            img_rd = cv2.rectangle(img_rd,
                                                   tuple([d.left(), d.top()]),
                                                   tuple([d.right(), d.bottom()]),
                                                   (0, 0, 255), 2)
                            
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()
                    for i in range(self.current_frame_face_cnt):            
                        text_info = f"Info: {self.current_frame_face_name_list[i]}"
                        if self.current_frame_face_name_list[i] != "unknown":
                            # Tạo tên file dựa trên tên của người dùng và các thông tin khác
                            for k, d in enumerate(faces):
                                self.current_frame_face_position_list.append(tuple(
                                    [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                                self.current_frame_face_centroid_list.append(
                                    [int(faces[k].left() + faces[k].right()) / 2,
                                    int(faces[k].top() + faces[k].bottom()) / 2])
                                left, top, right, bottom = d.left(), d.top(), d.right(), d.bottom()
                                face_img = img_rd[top:bottom, left:right]
                                img_rd = cv2.rectangle(img_rd,
                                                tuple([d.left(), d.top()]),
                                                tuple([d.right(), d.bottom()]),
                                                (0, 255, 0), 2)
                            
                            user_folder = os.path.join("X_Image_Tracking", self.current_frame_face_name_list[i])
                            os.makedirs(user_folder, exist_ok=True)
                            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                            face_save_path = os.path.join(user_folder, f"user_face_{self.current_frame_face_name_list[i]}_{current_time}_{self.frame_cnt}_{k}.jpg")
                            #TODO: Trường hợp đối tượng đã xác định - có trong dữ liệu hệ thống
                            if face_img is not None and face_img.size != 0:
                                cv2.imwrite(face_save_path, face_img)
                                id_checking = str(uuid.uuid4())
                                user_name = self.current_frame_face_name_list[i]
                                
                                log_to_google_sheets(id_checking, user_name, face_save_path)
                                
                                known_send_email(user_name, face_save_path)
                                
                            else:
                                print("Warning: face_img is empty, skipping save.")
                                  
                        else:
                            face_img = img_rd[top:bottom, left:right]
                            unknown_folder = os.path.join("X_Image_Tracking", "unknown")
                            os.makedirs(unknown_folder, exist_ok=True)
                            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                            face_save_path = os.path.join(unknown_folder, f"user_face_unkonwm_{current_time}_{self.frame_cnt}_{k}.jpg")      
                            if face_img is not None and face_img.size != 0:
                                cv2.imwrite(face_save_path, face_img)
                                id_checking = str(uuid.uuid4())
                                user_name = 'Uknown Person'
                                log_to_google_sheets(id_checking, user_name, face_save_path)
                                unknown_send_email(user_name, face_save_path)
                            else:
                                print("Warning: face_img is empty, skipping save.")
                            
                        cv2.putText(img_rd, text_info, 
                                    self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
                    self.draw_note(img_rd)
                    
                else:
                    logging.debug("scene 2: Faces cnt changes in this frame")
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0
                    if self.current_frame_face_cnt == 0:
                        logging.debug("  scene 2.1 No faces in this frame!!!")
                        self.current_frame_face_name_list = []
                    else:
                        logging.debug("  scene 2.2 Get faces in this frame and do face recognition")
                        self.current_frame_face_name_list = []
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                            self.current_frame_face_name_list.append("unknown") 
                        for k in range(len(faces)):
                            logging.debug("  For face %d in current frame:", k + 1)
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])
                            self.current_frame_face_X_e_distance_list = []
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            for i in range(len(self.face_features_known_list)):
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    e_distance_tmp = self.return_euclidean_distance(
                                        self.current_frame_face_feature_list[k],
                                        self.face_features_known_list[i])
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                else:
                                    self.current_frame_face_X_e_distance_list.append(999999999)
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                min(self.current_frame_face_X_e_distance_list))
                            # Max/Min Predictions
                            if min(self.current_frame_face_X_e_distance_list) < 0.35:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                                logging.debug("  Tracking Recognition Results: %s ",
                                              self.face_name_known_list[similar_person_num])
                            else:
                                logging.debug("  Tracking Recognition Results: Unknown person")

                if kk == ord('q'):
                    break
                self.update_fps()
                cv2.namedWindow("SafeX | Face Recognition Tracking System", 1)
                cv2.imshow("SafeX | Face Recognition Tracking System", img_rd)
                logging.debug("Frame Ends\n\n")

    def run(self):
        # URL RTSP IP Cam Ezviz C6N
        rtsp_url = "rtsp://admin:MRRZHJ@192.168.1.2:554/H.264"
        cap = cv2.VideoCapture(rtsp_url)
        
        # for test case cam reading
        # vid_dir = "X_Test_VP/case_5.mp4"
        # cap = cv2.VideoCapture(vid_dir)
        
        # cap = cv2.VideoCapture(0)              # Get video stream from camera
        # cap1 = cv2.VideoCapture(1)
        
        # Check error 
        if not cap.isOpened():
            logging.error("Warning: Failed to open RTSP stream.")
            return
        
        self.process(cap)
        # self.process(cap1)
        cap.release()
        cv2.destroyAllWindows()

def main():
    initialize_sheet()
    logging.basicConfig(level=logging.DEBUG) # Set log level to 'logging.DEBUG' to print debug info of every frame
    Face_Recognizer_con = Face_Recognizer()
    Face_Recognizer_con.run()

if __name__ == '__main__':
    main()

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
import math
# from X_Alert import X_Buzzer_Alarm

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
        #self.e_distance_accuracy = 0
        
    # Get data face landmark from csv file training
    def get_face_database(self):
        if os.path.exists("X_Center_Data/features_all.csv"):
            path_features_known_csv = "X_Center_Data/features_all.csv"
            # Reading
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
    
    # cal centroid track
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
        cv2.putText(img_rd, "Frame:  " + str(self.frame_cnt), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:    " + str(self.fps.__round__(2)), (20, 130), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Face:  " + str(self.current_frame_face_cnt), (20, 160), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Exit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        
        # aww u dont need turn on it, useless
        # for i in range(len(self.current_frame_face_name_list)):
        #     img_rd = cv2.putText(img_rd, "Face_" + str(i + 1), tuple(
        #         [int(self.current_frame_face_centroid_list[i][0]), int(self.current_frame_face_centroid_list[i][1])]),
        #                          self.font,
        #                          0.8, (255, 190, 0),
        #                          1,
        #                          cv2.LINE_AA)
        
    def descript(self, stream):
        while stream.isOpened():
            flag, img_rd = stream.read()
            self.frame_cnt+=1
            k = cv2.waitKey(1)
            print('- Frame ', self.frame_cnt, " starts:")
            timestamp1 = time.time()
            faces = detector(img_rd, 0)
            timestamp2 = time.time()
            print("--- Time used to `detector`:                  %s seconds ---" % (timestamp2 - timestamp1))
            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(faces) != 0:
                for face in faces:
                    timestamp3 = time.time()
                    face_shape = predictor(img_rd, face)
                    timestamp4 = time.time()
                    print("--- Time used to `predictor`:                 %s seconds ---" % (timestamp4 - timestamp3))
                    timestamp5 = time.time()
                    face_desc = face_reco_model.compute_face_descriptor(img_rd, face_shape)
                    timestamp6 = time.time()
                    print("--- Time used to `compute_face_descriptor：`   %s seconds ---" % (timestamp6 - timestamp5))

    def safe_pow(base, exp):
        try:
            return math.pow(base, exp)
        except ValueError as e:
            print(f"ValueError: {e} | base: {base}, exp: {exp}")
            return float('nan')  # Hoặc một giá trị phù hợp khác để xử lý trường hợp lỗi

    # support process
    def process(self, stream):
        if self.get_face_database():
            while stream.isOpened():
                self.frame_cnt += 1
                logging.debug("Frame " + str(self.frame_cnt) + " starts")
                flag, img_rd = stream.read()
                
                # Check if process cant take tuple 
                if not flag or img_rd is None:
                    logging.error("Failed to read frame %d", self.frame_cnt)
                    continue
                
                try:
                    # trying to resize camera frame
                    new_width = 640
                    new_height = 480
                    img_rd = cv2.resize(img_rd, (new_width, new_height))
                    
                except cv2.error as e:
                    logging.error("OpenCV error during resizing frame %d: %s", self.frame_cnt, e)
                    continue
                
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
                        # Put alert and process here
                        # X_Buzzer_Alarm(40, 1, 0.2, 3)
                        # Send data to cloud storage and notification
                        print("I dont know (test case 1: unknown per)")
                        
                        
                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])
                            img_rd = cv2.rectangle(img_rd,
                                                   tuple([d.left(), d.top()]),
                                                   tuple([d.right(), d.bottom()]),
                                                   (255, 255, 255), 2)
                            
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()
                    for i in range(self.current_frame_face_cnt):
                        # print(accuracy_text)
                        # print(self.e_distance_accuracy)
                        # text = f"Info: {self.current_frame_face_name_list[i]} \t Per: |{self.e_distance_accuracy:.2f}%|"
                        # text = f"Info: {self.current_frame_face_name_list[i]}\nPer: |{self.e_distance_accuracy:.2f}%|"
                        text = f"Info: {self.current_frame_face_name_list[i]}\nPer: |{self.e_distance_accuracy:.2f}%|"
                        

                        # Lấy kích thước của văn bản
                        text_width, text_height = cv2.getTextSize(text, self.font, 0.8, 1)[0]

                        # Thay thế "\n" bằng khoảng trống tương ứng với chiều cao của văn bản
                        # text = text.replace('\n', ' ' * text_height)
                        # img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i], 
                        #                      self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                        #                      cv2.LINE_AA)
                        # print(text)
                        # img_rd = cv2.putText(img_rd, text , 
                        #                      self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                        #                      cv2.LINE_AA)
                        
                        text_info = f"Info: {self.current_frame_face_name_list[i]}"
                        text_per = f"Per: |{self.e_distance_accuracy:.2f}%|"

                        # Vẽ văn bản cho Info
                        cv2.putText(img_rd, text_info, 
                                    self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

                        # Vẽ văn bản cho Per dựa trên vị trí của Info và chiều cao của văn bản
                        text_per_position = (self.current_frame_face_position_list[i][0], self.current_frame_face_position_list[i][1] + 30)
                        cv2.putText(img_rd, text_per, 
                                    text_per_position, self.font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

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
                                    
                                    def safe_pow(base, exp):
                                        try:
                                            return math.pow(base, exp)
                                        except ValueError as e:
                                            print(f"ValueError: {e} | base: {base}, exp: {exp}")
                                            return float('nan')  # Hoặc một giá trị phù hợp khác để xử lý trường hợp lỗi
                                        
                                    linear_val =(1.0 - e_distance_tmp)/ (0.4*2.0)
                                    if 0.0 <= linear_val <= 1.0:
                                        base = (linear_val - 0.5) * 2
                                        if base < 0 and 0.2 < 1:
                                            power_val = float('nan')  # Tránh giá trị âm không hợp lệ
                                        else:
                                            power_val = safe_pow(base, 0.2)

                                        self.e_distance_accuracy = (linear_val + ((1.0 - linear_val) * power_val)) * 100
                                    else:
                                        print(f"Invalid linear_val: {linear_val}")
                                        self.e_distance_accuracy = 0.0  # Hoặc một giá trị mặc định khác

                                    # self.e_distance_accuracy = (linear_val + ((1.0-linear_val)*math.pow((linear_val-0.5)*2,0.2)))*100 # error line
                                    logging.debug("Accuracy: with person %d, accuracy :%f%%",i+1, self.e_distance_accuracy)
                                    logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                    
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                    
                                    accuracy_text = f"Accuracy: {self.e_distance_accuracy:.2f}%"
                                    print(accuracy_text)
                                    
                                    
                                    
                                    
                                else:
                                    self.current_frame_face_X_e_distance_list.append(999999999)
                                    
                            # img_read = cv2.putText(img_rd, accuracy_text, (20,230), self.font, 0.8, (0,255,0), 1, cv2.LINE_AA)
                            # self.draw_note(img_read)
                                    
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                min(self.current_frame_face_X_e_distance_list))
                            
                            if min(self.current_frame_face_X_e_distance_list) < 0.35:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                                logging.debug("  Tracking Recognition Results: %s ",
                                              self.face_name_known_list[similar_person_num])
                            else:
                                logging.debug("  Tracking Recognition Results: Unknown person")

                        # 7. Add note on cv2 windowz
                        # Cap img
                        cv2.imwrite("debug/debug_" + str(self.frame_cnt) + ".png", img_rd) # Dump current frame image if needed

                # 8. Press 'q' to exit
                if kk == ord('q'):
                    break

                self.update_fps()
                cv2.namedWindow("SafeX | Face Recognition Tracking System", 1)
                cv2.imshow("SafeX | Face Recognition Tracking System", img_rd)

                logging.debug("Frame Ends\n\n")

    def run(self):
        # cap = cv2.VideoCapture("X_Test_VP/case_5.mp4")  # Get video stream from video file
        # URL RTSP IP Cam Ezviz C6N
        rtsp_url = "rtsp://admin:MRRZHJ@192.168.1.2:554/H.264"
        cap = cv2.VideoCapture(rtsp_url)
        # cap = cv2.VideoCapture(0)              # Get video stream from camera
        
        # Check error 
        if not cap.isOpened():
            logging.error("Warning: Failed to open RTSP stream.")
            return
        
        self.process(cap)
        # self.descript(cap)
        cap.release()
        cv2.destroyAllWindows()
    
    # print(descript(cap))

def main():
    logging.basicConfig(level=logging.DEBUG) # Set log level to 'logging.DEBUG' to print debug info of every frame
    logging.basicConfig(level=logging.INFO)
    Face_Recognizer_con = Face_Recognizer()
    Face_Recognizer_con.run()


if __name__ == '__main__':
    main()

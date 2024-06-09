# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import dlib
import numpy as np
import cv2
import os
import shutil
import time
import logging
import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk 
from tkinter import PhotoImage

detector = dlib.get_frontal_face_detector()

class Face_Register:
    def __init__(self):
        self.current_frame_faces_cnt = 0  # cnt for counting faces in current frame
        #self.current_frame_faces_cnt['fg'] = '#D7A7A6'
        self.existing_faces_cnt = 0
        #self.existing_faces_cnt['fg'] = '#D7A7A6'  # cnt for counting saved faces
        self.ss_cnt = 0  # person_n / cnt for screen shots

        # Tkinter GUI
        self.win = tk.Tk()
        self.win.title("Register SafeX | REAL-TIME SECURITY SYSTEM MODEL X")
        # PLease modify window size here if needed
        self.win.geometry("1300x800")
        self.win.resizable(False, False)

        # Save background
        self.background_image = PhotoImage(file="X_UI/Main_Register.png")  # Đường dẫn đến tệp ảnh nền
        self.background_label = tk.Label(self.win, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Đặt label full kích thước cửa sổ
        # self.background_label.pack(side="left", fill="y", expand="no" )

        # GUI left part
        self.frame_left_camera = tk.Frame(self.win)
        self.label = tk.Label(self.win)
        self.label.pack(side=tk.LEFT, padx=115)
        self.frame_left_camera.pack()

        # GUI right part
        #self.frame_right_info.create_rectangle(fill = '#1F2022')
        self.frame_right_info = tk.Frame(self.win, background='#07080A', highlightthickness = 0, highlightbackground='white', padx = 0, pady = 20)
        #self.frame_right_info - tk.Label(self.frame_right_info,background='black')
        self.label_cnt_face_in_database = tk.Label(self.frame_right_info, text=str(self.existing_faces_cnt),fg='#77B900',background='#07080A')
        self.label_cnt_face_in_database.grid(row=0, column=0)
        self.label_fps_info = tk.Label(self.frame_right_info, text="",fg='#77B900',background='#07080A')
        self.label_fps_info.grid(row=1, column=0)
        self.input_name = tk.Entry(self.frame_right_info)
        self.input_name.grid(row=2, column=0)
        self.input_name_char = ""
        self.label_warning = tk.Label(self.frame_right_info,fg='#77B900',background='#07080A')
        self.label_face_cnt = tk.Label(self.frame_right_info, text="Num of faces in the current frame: ",fg='#77B900',background='#07080A')
        self.log_all = tk.Label(self.frame_right_info,fg='#77B900',background='#07080A')
        #self.frame_right_info.grid(row=1, column=0, sticky=tk.S)  # Đặt frame ở dưới cùng
        self.frame_right_info.pack(pady=85)#,side="bottom")

        self.font_title = tkFont.Font(family='Helvetica', size=20, weight='bold')
        self.font_step_title = tkFont.Font(family='Helvetica', size=15, weight='bold')
        self.font_warning = tkFont.Font(family='Helvetica', size=15, weight='bold')

        self.path_photos_from_camera = "X_Center_Data/Face_Track_Data/"
        self.current_face_dir = ""
        self.font = cv2.FONT_ITALIC

        # Current frame and face ROI position
        self.current_frame = np.ndarray
        self.face_ROI_image = np.ndarray
        self.face_ROI_width_start = 0
        self.face_ROI_height_start = 0
        self.face_ROI_width = 0
        self.face_ROI_height = 0
        self.ww = 0
        self.hh = 0

        self.out_of_range_flag = False
        self.face_folder_created_flag = False
  
        # FPS
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        # self.img_bg = cv2.imread('uii/mainfr.png')
        self.cap = cv2.VideoCapture(0)  # Get video stream from camera
        # self.cap = cv2.VideoCapture('rtsp://admin:MRRZHJ@192.168.1.2:554/H.264') # Get video stream from camera
        # self.cap = cv2.VideoCapture("test.mp4")   # Input local video

    # Delete old face folders
    def GUI_clear_data(self):
        # Delete folder faces data was save: "/data_faces_from_camera/person_x/"...
        folders_rd = os.listdir(self.path_photos_from_camera)
        for i in range(len(folders_rd)):
            shutil.rmtree(self.path_photos_from_camera + folders_rd[i])
        if os.path.isfile("X_Center_Data/features_all.csv"):
            os.remove("X_Center_Data/features_all.csv")
        self.label_cnt_face_in_database['text'] = "0"
        #self.label_cnt_face_in_database['fg'] = '#D7A7A6'
        self.existing_faces_cnt = 0
        #self.existing_faces_cnt['fg'] = '#D7A7A6'
        self.log_all["text"] = "Deleted facial biometric data in `features_all.csv`"

    def GUI_get_input_name(self):
        self.input_name_char = self.input_name.get()
        self.create_face_folder()
        self.label_cnt_face_in_database['text'] = str(self.existing_faces_cnt)
        #self.label_cnt_face_in_database['fg'] = '#D7A7A6'

    def GUI_info(self):
        tk.Label(self.frame_right_info,
                 text="Register Biometric Data \n Welcome To SafeX - Sign Up",fg="White",background='#07080A',
                 font=self.font_title).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=2, pady=20)

        tk.Label(self.frame_right_info,
                 text="FPS: ",fg='White',background='#07080A').grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
        self.label_fps_info.grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)

        tk.Label(self.frame_right_info,
                 text="Faces in archived data: ",background='#07080A',fg='White').grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
        self.label_cnt_face_in_database.grid(row=2, column=2, columnspan=3, sticky=tk.W, padx=5, pady=2)

        tk.Label(self.frame_right_info,
                 text="Face in current frame: ",fg='White',background='#07080A').grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
        self.label_face_cnt.grid(row=3, column=2, columnspan=3, sticky=tk.W, padx=5)#, pady=2)

        self.label_warning.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5)#, pady=2)

        # Step 1: Clear old data
        tk.Label(self.frame_right_info,
                 font=self.font_step_title,
                 text=" Delete face photo",fg='White',background='#07080A').grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5)#, pady=20)
        tk.Button(self.frame_right_info,
                  text='Delete',fg='Black', justify = 'center', anchor = 'center', 
                  command=self.GUI_clear_data,background='#77B900', border = 5, borderwidth = 2, font=('Helvetica', 11, ' bold '), activebackground = "#3F6200", activeforeground = "White").grid(row=6, column=0, columnspan=3, sticky=tk.W, padx=5)#, pady=2)

        # Step 2: Input name and create folders for face
        tk.Label(self.frame_right_info,
                 font=self.font_step_title,
                 text=" Enter username",fg='White',background='#07080A').grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5)#, pady=20)

        tk.Label(self.frame_right_info, text="Username: ",fg='#77B900',background='#07080A').grid(row=8, column=0, sticky=tk.W, padx=5, pady=0)
        self.input_name.grid(row=8, column=1, sticky=tk.W, padx=0, pady=2)

        tk.Button(self.frame_right_info,
                  text='Enter',fg='Black', justify = 'center', anchor = 'center', 
                  command=self.GUI_get_input_name, background='#77B900', border = 5, borderwidth = 2, font=('Helvetica', 11, ' bold '), activebackground = "#3F6200", activeforeground = "White").grid(row=8, column=2, padx=5)

        # Step 3: Save current face in frame
        tk.Label(self.frame_right_info,
                 font=self.font_step_title,
                 text=" Save face image",fg='White',background='#07080A').grid(row=9, column=0, columnspan=2, sticky=tk.W, padx=5)#, pady=20)

        tk.Button(self.frame_right_info,
                  text='Save current face', fg='Black', justify = 'center', anchor = 'center', 
                  command=self.save_current_face, background='#77B900', border = 5, borderwidth = 2, font=('Helvetica', 11, ' bold '), activebackground = "#3F6200", activeforeground = "White").grid(row=10, column=0, columnspan=3, sticky=tk.W)

        tk.Button(self.frame_right_info,
                  text='Exit', fg='Black', justify = 'center', anchor = 'center', 
                  command=self.out_X_Register, background='#77B900', border = 5, borderwidth = 2, font=('Helvetica', 11, ' bold '), activebackground = "#3F6200", activeforeground = "White").grid(row=11, column=0, columnspan=3, sticky=tk.W)
        
        # Show log in GUI
        self.log_all.grid(row=11, column=0, columnspan=20, sticky=tk.W, padx=5, pady=16)

        self.frame_right_info.pack(side=tk.BOTTOM)
    
    def out_X_Register(self):
        self.win.destroy()

    # Mkdir for saving photos and csv
    def pre_work_mkdir(self):
        # Create folders to save face images and csv
        if os.path.isdir(self.path_photos_from_camera):
            pass
        else:
            os.mkdir(self.path_photos_from_camera)

    # Start from person_x+1
    def check_existing_faces_cnt(self):
        if os.listdir("X_Center_Data/Face_Track_Data/"):
            # Get the order of latest person
            person_list = os.listdir("X_Center_Data/Face_Track_Data/")
            person_num_list = []
            for person in person_list:
                person_order = person.split('_')[1].split('_')[0]
                person_num_list.append(int(person_order))
            self.existing_faces_cnt = max(person_num_list)
        else:
            self.existing_faces_cnt = 0

    # Update FPS of Video stream
    def update_fps(self):
        now = time.time()
        # Refresh fps per second
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

        self.label_fps_info["text"] = str(self.fps.__round__(2))

    def create_face_folder(self):
        # Create the folders for saving faces
        self.existing_faces_cnt += 1
        if self.input_name_char:
            self.current_face_dir = self.path_photos_from_camera + \
                                    "person_" + str(self.existing_faces_cnt) + "_" + \
                                    self.input_name_char
        else:
            self.current_face_dir = self.path_photos_from_camera + \
                                    "person_" + str(self.existing_faces_cnt)
        os.makedirs(self.current_face_dir)
        self.log_all["text"] = "Created data at \n" + self.current_face_dir 
        logging.info("\n%-40s %s", "Create data at:", self.current_face_dir)

        self.ss_cnt = 0  # Clear the cnt of screen shots
        self.face_folder_created_flag = True  # Face folder already created

    def save_current_face(self):
        if self.face_folder_created_flag:
            if self.current_frame_faces_cnt == 1:
                if not self.out_of_range_flag:
                    self.ss_cnt += 1
                    # Create blank image according to the size of face detected
                    self.face_ROI_image = np.zeros((int(self.face_ROI_height * 2), self.face_ROI_width * 2, 3),
                                                   np.uint8)
                    for ii in range(self.face_ROI_height * 2):  
                        for jj in range(self.face_ROI_width * 2):
                            self.face_ROI_image[ii][jj] = self.current_frame[self.face_ROI_height_start - self.hh + ii][
                                self.face_ROI_width_start - self.ww + jj]
                    self.log_all["text"] = "Saved data at \n" + self.current_face_dir + "/img_face_" + str(
                        self.ss_cnt) + ".jpg\"" 
                    self.face_ROI_image = cv2.cvtColor(self.face_ROI_image, cv2.COLOR_BGR2RGB)

                    cv2.imwrite(self.current_face_dir + "/img_face_" + str(self.ss_cnt) + ".jpg", self.face_ROI_image)
                    logging.info("%-40s %s/img_face_%s.jpg", "Saved data at： ",
                                 str(self.current_face_dir), str(self.ss_cnt) + ".jpg")
                else:
                    self.log_all["text"] = "Notice: Please do not leave the detection range!"
            else:
                self.log_all["text"] = "Warning: No face detected in current frame!"
        else:
            self.log_all["text"] = "Notice: Please skip to step 2!"

    def get_frame(self):
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    return None
                new_width = 640  
                new_height = 480  
                frame = cv2.resize(frame, (new_width, new_height))
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return None, None
        except Exception as e:
            print(f"Error: No input video!!! Exception: {e}")
            return None, None

    # Main process of face detection and saving
    def process(self):
        ret, self.current_frame = self.get_frame()
        if ret is None or self.current_frame is None:
            print("Failed to get frame")
            time.sleep(1)
        
        faces = detector(self.current_frame, 0)
        # Get frame
        if ret:
            self.update_fps()
            self.label_face_cnt["text"] = str(len(faces))
            # Face detected
            if len(faces) != 0:
                # Show the ROI of faces
                for k, d in enumerate(faces):
                    self.face_ROI_width_start = d.left()
                    self.face_ROI_height_start = d.top()
                    # Compute the size of rectangle box
                    self.face_ROI_height = (d.bottom() - d.top())
                    self.face_ROI_width = (d.right() - d.left())
                    self.hh = int(self.face_ROI_height / 2)
                    self.ww = int(self.face_ROI_width / 2)
                    # If the size of ROI > 480x640
                    if (d.right() + self.ww) > 640 or (d.bottom() + self.hh > 480) or (d.left() - self.ww < 0) or (
                            d.top() - self.hh < 0):
                        self.label_warning["text"] = "OUT OF THE RANGE OF IDENTIFICATION"
                        self.label_warning['fg'] = 'red'
                        self.out_of_range_flag = True
                        color_rectangle = (255, 0, 0)
                    else:
                        self.out_of_range_flag = False
                        self.label_warning["text"] = "WITHIN THE SCOPE OF IDENTIFICATION"
                        self.label_warning['fg'] = 'light green'
                        color_rectangle = (255, 255, 255)
                    self.current_frame = cv2.rectangle(self.current_frame,
                                                       tuple([d.left() - self.ww, d.top() - self.hh]),
                                                       tuple([d.right() + self.ww, d.bottom() + self.hh]),
                                                       color_rectangle, 2)
            self.current_frame_faces_cnt = len(faces)

            # Convert PIL.Image.Image to PIL.Image.PhotoImage
            img_Image = Image.fromarray(self.current_frame)
            img_PhotoImage = ImageTk.PhotoImage(image=img_Image)
            self.label.img_tk = img_PhotoImage
            self.label.configure(image=img_PhotoImage)

        # Refresh frame
        self.win.after(20, self.process)

    def run(self):
        self.pre_work_mkdir()
        self.check_existing_faces_cnt()
        self.GUI_info()
        self.process()
        self.win.mainloop()

def show_infor(text, delay=0.05):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print() 
        
def main():
    logging.basicConfig(level=logging.INFO)
    Face_Register_con = Face_Register()
    Face_Register_con.run()

if __name__ == '__main__':
    main()

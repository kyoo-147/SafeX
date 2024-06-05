# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import tkinter as tk
from tkinter import Message ,Text
from PIL import Image, ImageTk
import pandas as pd
from tkinter import font as tkFont
from tkinter import PhotoImage 
import time
import tkinter.ttk as ttk
import subprocess
import logging

class X_Main():
    def __init__(self):
        # Create info ui
        #self.master = master
        self.xmain = tk.Tk()
        self.xmain.title("SafeX | REAL-TIME SECURITY SYSTEM MODEL X")
        self.xmain.geometry("1300x800")
        self.xmain.resizable(False, False)
        # Background main x
        self.background_image = PhotoImage(file="X_UI/Main_Bg.png")
        self.background_label = tk.Label(self.xmain, image=self.background_image, bg="#1F2022", background="#1F2022")
        self.background_label.place(relwidth=1, relheight=1)
        # Main gui
        # self.xmain.attributes('-fullscreen', True) # setting fullscreen image
        self.button_X_Register = tk.Button(self.xmain, text="Register", command=self.open_X_Register, fg="white", highlightthickness = 0, font=('Helvetica', 15, ' bold '), anchor='sw',justify='left',borderwidth=0  ,width = 10  , height=0 , activebackground = "#07080A", activeforeground = "#77B900" , background="#07080A")#.grid(row=8, column=2, padx=5)
        self.button_X_Register.place(x = 328, y = 188)
        self.button_X_Register = tk.Button(self.xmain, text="Training",command=self.open_X_Training,fg="white", highlightthickness = 0, font=('Helvetica', 15, ' bold '), anchor='sw',justify='left',borderwidth=0  ,width = 10  , height = 0 , activebackground = "#07080A", activeforeground = "#77B900" , background="#07080A")#.grid(row=8, column=2, padx=5)
        self.button_X_Register.place(x = 328, y = 302)
        self.button_X_Recognition = tk.Button(self.xmain, text="Recognition",command=self.open_X_Recog, fg="white", highlightthickness = 0, font=('Helvetica', 15, ' bold '), anchor='sw',justify='left' , borderwidth=0    ,width=10  , height = 0, activebackground = "#07080A", activeforeground = "#77B900" , background="#07080A")
        self.button_X_Recognition.place(x = 328, y = 418)
        self.button_X_Out = tk.Button(self.xmain, text="Exit",command=self.out_X_Main, fg="white", highlightthickness = 0, font=('Helvetica', 15, ' bold '), anchor='sw',justify='left' , borderwidth=0    ,width = 10  ,height = 0, activebackground = "#07080A", activeforeground = "#77B900" , background="#07080A")
        self.button_X_Out.place(x = 328, y = 532)
    # Open X_Register Part---
    def open_X_Register(self):
        show_infor("------   REGISTER STARTING ALREADY | Look at your camera and smile ", delay = 0.03)
        show_infor("---------        Always keep your face in the frame, this will be quick, but we require precision.", delay = 0.01)
        show_infor("---------        We recommend having 20-35 images in your database", delay = 0.01)
        self.X_Register_Path = "X_Register.py"
        subprocess.call(['python3', self.X_Register_Path])
    # Open X_Training Part---
    def open_X_Training(self):
        show_infor("------   TRAINING STARTING ALREADY | Relax and check the information again ", delay = 0.03)
        show_infor("---------        This process will take a little time for the machine to work.", delay = 0.01)
        show_infor("---------        You will receive an activity notification when it is complete", delay = 0.01)
        self.X_Training_Path = "X_Training.py"
        subprocess.call(['python3', self.X_Training_Path])
    def open_X_Recog(self):
        show_infor("------   RECOGNITION STARTING ALREADY | Open your horizons ", delay = 0.03)
        show_infor("---------        We will always keep your safety and information up to date.", delay = 0.01)
        show_infor("---------        All information will be stored in our cloud, please visit: ...(link will update soon)", delay = 0.01)
        self.X_Recog_OT_Path = "X_Optimize.py"
        subprocess.call(['python3', self.X_Recog_OT_Path])
    # Out X_Main Program---
    def out_X_Main(self):
        self.xmain.destroy()
        show_infor("------   SafeX HAS BEEN DISCONTINUED | Thank you for the process of use ", delay = 0.03)
        show_infor("---------        We recommend that you do not arbitrarily turn off or disconnect the system suddenly.", delay = 0.01)
        show_infor("---------        Doing so will be dangerous for you and your system. You should only stop doing so with technical supervision or a system upgrade.", delay = 0.01)
        show_infor("Thank you for trusting and using | We will always keep you and your family safe", delay = 0.03)
        show_infor("Copyright © 2024 NaVin AIF. All rights reserved.", delay = 0.04)
    def run(self):
        self.xmain.mainloop()

def show_infor(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()    

def main():
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(filename="X_Log_Info/Tracking_System_Real_Time.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Debug has been started")
    logging.info("The program works")
    logging.warning("An unexpected situation has been detected, but the program continues to operate")
    logging.error("Detect serious errors that affect program operations")
    logging.critical("If an extremely serious error is detected, the program will stop immediately")
    running = X_Main()
    running.run()

if __name__ == "__main__":
    show_infor("SafeX | REAL-TIME SECURITY SYSTEM MODEL X")
    show_infor("Developed by NaVin AIF Technology Company")
    show_infor("Copyright © 2024 NaVin AIF. All rights reserved.")
    print("*************************************************************************")
    show_infor("Open your smart vision | Always keep you safe", delay = 0.02)
    show_infor("Free to use. Easy to test. Just installing it can help with everything about security and more.", delay = 0.02)
    show_infor("AI Features", delay = 0.01)
    show_infor("    Identity & Access Control and Vehicle Management", delay = 0.01)
    show_infor("    Cloud storage & Data retrieval", delay = 0.01)
    show_infor("    Safety & Security Monitoring", delay = 0.01)
    show_infor("SafeX can make some mistakes. Be considerate and always check important information. We will try to improve it.", delay = 0.02)
    print("*************************************************************************")
    # running main thread
    main()






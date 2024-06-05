# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import cv2
import os
import uuid

def save_image(frame, face_location, name):
    top, right, bottom, left = face_location
    face_image = frame[top:bottom, left:right]

    directory = f'X_Image_Tracking/{name}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    image_path = f'{directory}/{uuid.uuid4()}.jpg'
    cv2.imwrite(image_path, face_image)
    return image_path

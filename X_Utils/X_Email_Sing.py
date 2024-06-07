# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)

# Lưu ý về bảo mật: Lưu mật khẩu trong mã nguồn là không an toàn và có thể dẫn đến rủi ro bảo mật. Hãy cân nhắc các biện pháp thay thế như: Sử dụng biến môi trường để lưu mật khẩu và truy xuất trong mã. Sử dụng file cấu hình được mã hóa và giải mã mật khẩu khi chạy mã.

# import smtplib
# from email.mime.text import MIMEText

# def send_email(name):
#     sender = "ngoctuanvinh1332@gmail.com"
#     receiver = "minhcuongdeptraine@gmail.com"
#     password = "otmn dyaw kimc inxc"

#     message = MIMEText(f"A face was recognized: {name}")
#     message["Subject"] = "[NaVin Warning]:Face Recognition Alert"
#     message["From"] = sender
#     message["To"] = receiver

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(sender, password)
#         server.sendmail(sender, receiver, message.as_string())
#         print("Email sent successfully.")

# name = 'Uknown'
# send_email(name)


# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# import os

# def send_email(name, image_path):
#     sender = "ngoctuanvinh1332@gmail.com"
#     receiver = "minhcuongdeptraine@gmail.com"
#     # password = "otmn dyaw kimc inxc"  # Thay thế bằng mật khẩu ứng dụng của bạn
#     # Security with password enviroment, you can set in your enviroment
#     password = os.getenv("EMAIL_PASSWORD_SENT") 

#     subject = "[NaVin Warning]: Unidentified object detection warning"
#     body = f"A face was recognized: {name}"

#     message = MIMEMultipart()
#     message["From"] = sender
#     message["To"] = receiver
#     message["Subject"] = subject

#     message.attach(MIMEText(body, "plain"))

#     # Attach image
#     try:
#         with open(image_path, 'rb') as img_file:
#             img = MIMEImage(img_file.read())
#             img.add_header('Content-Disposition', 'attachment', filename=image_path)
#             message.attach(img)
#     except FileNotFoundError:
#         print(f"Failed to attach image. File {image_path} not found.")
#         return

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender, password)
#             server.sendmail(sender, receiver, message.as_string())
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email. Error: {e}")

# name = 'Unknown'
# image_path = 'X_Image_Tracking/unknown/user_face_unkonwm_20240606_162553_835_6.jpg'  # Thay bằng đường dẫn tới hình ảnh của bạn
# send_email(name, image_path)



# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# import os
# from datetime import datetime

# def send_email(name, image_path):
#     sender = "ngoctuanvinh1332@gmail.com"
#     receiver = "minhcuongdeptraine@gmail.com"
#     password = "otmn dyaw kimc inxc"  # Thay thế bằng mật khẩu ứng dụng của bạn

#     subject = "[NaVin Warning]: Face Recognition Alert"
#     body = f"""
#     <html>
#     <body>
#         <p>Hello,</p>
#         <p>A face was recognized: {name}.</p>
#         <p>Here are the details:</p>
#         <ul>
#             <li>Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
#             <li>Location: Main Entrance</li>
#         </ul>
#         <p>Please find the attached image for your reference.</p>
#         <br>
#         <p>Best regards,<br>
#         Security Team</p>
#         <hr>
#         <p><b>Work With Andrew Ng</b></p>
#         <p>Join the teams that are bringing AI to the world! Check out job openings at <a href="https://www.deeplearning.ai">DeepLearning.AI</a>, AI Fund, and Landing AI.</p>
#         <p>Subscribe and view previous issues <a href="https://www.deeplearning.ai/thebatch">here</a>.</p>
#         <p>Thoughts, suggestions, feedback? Please send to <a href="mailto:thebatch@deeplearning.ai">thebatch@deeplearning.ai</a>. Avoid our newsletter ending up in your spam folder by adding our email address to your contacts list.</p>
#         <p>DeepLearning.AI, 195 Page Mill Road, Suite 115, Palo Alto, CA 94306, United States</p>
#         <p><a href="https://www.deeplearning.ai/unsubscribe">Unsubscribe</a> | <a href="https://www.deeplearning.ai/manage-preferences">Manage preferences</a></p>
#     </body>
#     </html>
#     """

#     message = MIMEMultipart()
#     message["From"] = sender
#     message["To"] = receiver
#     message["Subject"] = subject

#     message.attach(MIMEText(body, "html"))

#     # Attach image
#     try:
#         with open(image_path, 'rb') as img_file:
#             img = MIMEImage(img_file.read())
#             img.add_header('Content-Disposition', 'attachment', filename=image_path)
#             message.attach(img)
#     except FileNotFoundError:
#         print(f"Failed to attach image. File {image_path} not found.")
#         return

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender, password)
#             server.sendmail(sender, receiver, message.as_string())
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email. Error: {e}")

# name = 'Unknown'
# image_path = 'X_Image_Tracking/unknown/user_face_unkonwm_20240606_162550_831_6.jpg'  # Thay bằng đường dẫn tới hình ảnh của bạn
# send_email(name, image_path)



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from datetime import datetime

def send_email(name, image_path):
    sender = "ngoctuanvinh1332@gmail.com"
    receiver = "minhcuongdeptraine@gmail.com"
    password = os.getenv("EMAIL_PASSWORD_SENT")  # Lấy mật khẩu từ biến môi trường

    subject = "[NaVin Warning]: Face Recognition Alert"
    body = f"""
    <html>
    <body>
        <table style="background-color: #78BA01; color: #000000; width: 100%;">
            <tr>
                <td style="padding: 10px;"><img src="cid:company_logo" alt="Company Logo" style="width:100px;height:100px;"></td>
                <td style="padding: 10px;">
                    <h1 style="margin: 0;">NaVin AIF Technology Company Cloud Data Center</h1>
                    <h2 style="margin: 0;">Our Body Of Work</h2>
                </td>
            </tr>
        </table>
        <h3>Notification: Suspicious Activity Alert</h3>
        <p>Potentially compromised credentials for Google Cloud Platform/API project safex-003</p>
        <p>Hello,</p>
        <p>A face was recognized: {name}.</p>
        <p>Here are the details:</p>
        <ul>
            <li>Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            <li>Location: Main Entrance</li>
        </ul>
        <p>Please find the attached image for your reference.</p>
        <br>
        <p>Best regards,<br>Security Team Trust & Safety</p>
        <hr>
        <p><b>Work With Andrew Ng</b></p>
        <p>Join the teams that are bringing AI to the world! Check out job openings at <a href="https://www.deeplearning.ai">DeepLearning.AI</a>, AI Fund, and Landing AI.</p>
        <p>Subscribe and view previous issues <a href="https://www.deeplearning.ai/thebatch">here</a>.</p>
        <p>Thoughts, suggestions, feedback? Please send to <a href="mailto:thebatch@deeplearning.ai">thebatch@deeplearning.ai</a>. Avoid our newsletter ending up in your spam folder by adding our email address to your contacts list.</p>
        <p>DeepLearning.AI, 195 Page Mill Road, Suite 115, Palo Alto, CA 94306, United States</p>
        <p><a href="https://www.deeplearning.ai/unsubscribe">Unsubscribe</a> | <a href="https://www.deeplearning.ai/manage-preferences">Manage preferences</a></p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    # Attach HTML body
    message.attach(MIMEText(body, "html"))

    # Attach company logo
    try:
        with open("X_Test/Image/X_Logo.png", 'rb') as logo_file:
            logo = MIMEImage(logo_file.read())
            logo.add_header('Content-ID', '<company_logo>')
            message.attach(logo)
    except FileNotFoundError:
        print("Failed to attach logo. File not found.")
        return

    # Attach image of detected face
    try:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename=image_path)
            message.attach(img)
    except FileNotFoundError:
        print(f"Failed to attach image. File {image_path} not found.")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

name = 'Unknown'
image_path = 'X_Image_Tracking/unknown/user_face_unkonwm_20240606_162550_830_6.jpg'  # Thay bằng đường dẫn tới hình ảnh của bạn
send_email(name, image_path)



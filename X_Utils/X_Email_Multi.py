# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from datetime import datetime

def get_receiver_emails(file_path):
    with open(file_path, 'r') as file:
        emails = [line.strip() for line in file if line.strip()]
    return emails

def unknown_send_email(name, image_path):
    # Admin Email
    sender = "ngoctuanvinh1332@gmail.com"
    receivers = get_receiver_emails("X_Utils/Receivers_User.txt")  
    location = "Lot E2, Yen Hoa New Urban Area - Cau Giay - Hanoi"
    # Get security password from Enviroment Ubuntu
    password = os.getenv("EMAIL_PASSWORD_SENT")  

    subject = "[NaVin Warning]: Unidentified object detection warning"
    body = f"""
    <html>
    <body >
        <table style="background-color: #78BA01; color: #000000; width: 100%;">
            <tr>
                <td style="padding: 10px; "><img src="cid:company_logo" alt="Company Logo" style="width:100px;height:100px;"></td>
                <td style="padding: 10px;">
                    <h1 style="margin: 0; font-size: 24px;">NaVin AIF Technology Company Cloud Data Center</h1>
                    <h2 style="margin: 0; font-size: 15px;">Our Body Of Work</h2>
                </td>
            </tr>
        </table>
        <h3>Notification: Warning detects objects not in the system with suspicious activity</h3>
        <p>Potentially compromised credentials for the SafeX Model X system (Note: Need to double check unknown object information)</p>
        <p>Hello, User</p>
        <p>The SafeX system has detected an unknown object: {name}.</p>
        <p>Here are the details:</p>
        <ul>
            <li>Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            <li>Location: {location}</li>
        </ul>
        <p>Please see attached detailed facial images to make the quickest decisions. If the detection time is too long, the system will activate the dangerous alarm mode.</p>
        <br>
        <p>Best regards,<br>Security Team Trust & Safety</p>
        <hr>
        <p><b>NaVin AIF Technology Company</b></p>
        <p>Let us help protect your safety! See detailed information about the demo at <a href="https://www.youtube.com/@NaVin_AIF_Tech/featured">NaVin AIF</a>, Trust, and Safety.</p>
        <p>Subscribe and view previous issues <a href="mailto:ngoctuanvinh1332@gmail.com">here</a>.</p>
        <p>Thoughts, upgrades, maintenance, feedback? Please send it <a href="mailto:ngoctuanvinh1332@gmail.com">NaVin AIF</a>. To avoid our newsletter falling into the spam folder causing security disruption, by adding our email address to your contact list.</p>
        <p>NaVin AIF Technology Company, Ho Chi Minh City, VietNam</p>
        <p><a href="https://www.youtube.com/@NaVin_AIF_Tech/featured">Youtube</a> | <a href="https://github.com/kyoo-147">Github</a></p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(receivers)  # Gộp danh sách địa chỉ email thành một chuỗi ngăn cách bởi dấu phẩy
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
            server.sendmail(sender, receivers, message.as_string())  # Sử dụng danh sách receivers
        print("[NaVin Notifications]: Email sent successfully.")
    except Exception as e:
        print(f"[NaVin Warning]: Failed to send email. Error: {e}")

def known_send_email(name, image_path):
    # Admin Email
    sender = "ngoctuanvinh1332@gmail.com"
    receivers = get_receiver_emails("X_Utils/Receivers_User.txt")  
    location = "Lot E2, Yen Hoa New Urban Area - Cau Giay - Hanoi"
    # Get security password from Enviroment Ubuntu
    password = os.getenv("EMAIL_PASSWORD_SENT")  

    subject = "[NaVin Notification]: Notice of object detection in system data"
    body = f"""
    <html>
    <body >
        <table style="background-color: #78BA01; color: #000000; width: 100%;">
            <tr>
                <td style="padding: 10px; "><img src="cid:company_logo" alt="Company Logo" style="width:100px;height:100px;"></td>
                <td style="padding: 10px;">
                    <h1 style="margin: 0; font-size: 24px;">NaVin AIF Technology Company Cloud Data Center</h1>
                    <h2 style="margin: 0; font-size: 15px;">Our Body Of Work</h2>
                </td>
            </tr>
        </table>
        <h3>Notification: Notification that an object has been detected in the system within the range that can be received</h3>
        <p>Authentication information will be stored and behavior monitored (Note: Need to carefully check subject information to confirm behavior)</p>
        <p>Hello, User</p>
        <p>The SafeX system has detected the specified object: {name}.</p>
        <p>Here are the details:</p>
        <ul>
            <li>Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            <li>Location: {location}</li>
        </ul>
        <p>Please see attached detailed facial image to confirm. If the detection time is too long, the system will notify you about the confirmation status.</p>
        <br>
        <p>Best regards,<br>Security Team Trust & Safety</p>
        <hr>
        <p><b>NaVin AIF Technology Company</b></p>
        <p>Let us help protect your safety! See detailed information about the demo at <a href="https://www.youtube.com/@NaVin_AIF_Tech/featured">NaVin AIF</a>, Trust, and Safety.</p>
        <p>Subscribe and view previous issues <a href="mailto:ngoctuanvinh1332@gmail.com">here</a>.</p>
        <p>Thoughts, upgrades, maintenance, feedback? Please send it <a href="mailto:ngoctuanvinh1332@gmail.com">NaVin AIF</a>. To avoid our newsletter falling into the spam folder causing security disruption, by adding our email address to your contact list.</p>
        <p>NaVin AIF Technology Company, Ho Chi Minh City, VietNam</p>
        <p><a href="https://www.youtube.com/@NaVin_AIF_Tech/featured">Youtube</a> | <a href="https://github.com/kyoo-147">Github</a></p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(receivers)  # Gộp danh sách địa chỉ email thành một chuỗi ngăn cách bởi dấu phẩy
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
            server.sendmail(sender, receivers, message.as_string())  # Sử dụng danh sách receivers
        print("[NaVin Notifications]: Email sent successfully.")
    except Exception as e:
        print(f"[NaVin Warning]: Failed to send email. Error: {e}")
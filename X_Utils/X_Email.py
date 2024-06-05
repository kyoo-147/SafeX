# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import smtplib
from email.mime.text import MIMEText

def send_email(name):
    sender = "ngoctuanvinh1332@gmail.com"
    receiver = "baemyungkang2806@gmail.com"
    password = ""

    message = MIMEText(f"A face was recognized: {name}")
    message["Subject"] = "[NaVin Warning]:Face Recognition Alert"
    message["From"] = sender
    message["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 25) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())

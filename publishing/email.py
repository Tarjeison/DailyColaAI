import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_email_with_image_attachment(img_path: str, username: str, password: str,
                                     email_sender: str, email_recipient: str,
                                     server: str = 'smtp.gmail.com', port: str = '587'):
    img_data = open(img_path, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Daily update'

    text = MIMEText("Beep boop. Here is a Cola... (I hope)... Beep.")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img_path))
    msg.attach(image)

    s = smtplib.SMTP(server, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(username, password)
    s.sendmail(email_sender, email_recipient, msg.as_string())
    s.quit()

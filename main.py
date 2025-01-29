import time
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO
import subprocess

toaddr = 'abc@gmail.com'
me = 'xyz@gmail.com'
password = 'wqen yqil ouih alvt'  # Use the app password here
subject = 'Security alert'
image_path = '/home/pi/my_image1.jpg'

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

while True:
    if GPIO.input(23):
        print('Motion detected')
        time.sleep(2)
       
        # Capture image
        try:
            subprocess.run(['fswebcam', '-d', '/dev/video0', image_path], check=True)
            print(f"Image Captured: {image_path}")
        except subprocess.CalledProcessError:
            print("Failed to capture image")
            continue

        # Prepare the email
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
       
        with open(image_path, 'rb') as fp:
            img = MIMEImage(fp.read())
            msg.attach(img)
       
        # Send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(me, password)
            server.send_message(msg)
            server.quit()
            print('Email sent')
        except Exception as e:  # Fix here
            print(f"Failed to send email: {e}")
            time.sleep(10)

GPIO.cleanup()

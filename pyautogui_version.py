import datetime
import os
import pyautogui
import time
import smtplib
from email.mime.text import MIMEText
from PIL import Image
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from datetime import datetime


load_dotenv()


from_email = os.getenv("FROM_EMAIL")
to_email = os.getenv("TO_EMAIL")
password = os.getenv("PASSWORD")


def send_email_alert():
    msg = MIMEText("Custom indicator signal detected on TradingView!")
    msg['Subject'] = 'TradingView Alert'
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())


Tk().withdraw()
image_path = askopenfilename()

region = (0, 0, 1920, 1080)


try:
    image = Image.open(image_path)
except IOError:
    print(f"Unable to open image file: {image_path}")
    exit(1)

try:
    while True:
        screenshot = pyautogui.screenshot(region=region)

        try:
            signal_location = pyautogui.locate(image_path, screenshot, confidence=0.8)
            indicator_appeared = datetime.now()
        except pyautogui.ImageNotFoundException:
            signal_location = None

        if signal_location:
            send_email_alert()
            messagebox.showinfo("Indicator appeared", f"The indicator have just appeared in the chart at {indicator_appeared}")

        time.sleep(60)
except KeyboardInterrupt:
    print("Monitoring stopped.")

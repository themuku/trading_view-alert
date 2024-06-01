import os

import pyautogui
import http.client
import time
import urllib
from datetime import datetime

import pyautogui
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("USER")
token = os.getenv("TOKEN")


def send_push(msg):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": token,
                     "user": user,
                     "title": "Trading",
                     "sound": "echo",
                     "priority": 2,
                     "retry": 30,
                     "expire": 10800,
                     "message": msg,
                 }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()


buy_img = "./buy.jpg"
sell_img = "./sell.jpg"

region = (0, 0, 1920, 1080)


try:
    while True:
        screenshot = pyautogui.screenshot(region=region)

        try:
            buy_signal_location = pyautogui.locate(buy_img, screenshot, confidence=0.8)
            sell_signal_location = pyautogui.locate(sell_img, screenshot, confidence=0.8)
            indicator_appeared = datetime.now()
        except pyautogui.ImageNotFoundException:
            buy_signal_location = None
            sell_signal_location = None

        if buy_signal_location:
            send_push("Buy signal")

        if sell_signal_location:
            send_push("Sell signal")

        time.sleep(60)
except KeyboardInterrupt:
    print("Monitoring stopped.")

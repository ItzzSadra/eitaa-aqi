import time
import requests
from aqi import get_aqi
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def get_aqi_function():
    EITAA_API_KEY = os.getenv('EITAA_API_KEY')
    current_time = datetime.now().strftime("%H:%M")
    print(current_time)
    CHAT_ID = "10964115"
    data = f""
    URL = f"https://eitaayar.ir/api/{EITAA_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={data}&date=0&parse_mode=&pin=on&viewCountForDelete="
    aqi = get_aqi("Isfahan")


def countdown(hours=1):
    total_seconds = hours * 3600
    try:
        while total_seconds:
            mins, secs = divmod(total_seconds, 60)
            hours_left, mins = divmod(mins, 60)
            timer = f"{hours_left:02d}:{mins:02d}:{secs:02d}"
            print(f"\rNext run in: {timer}", end="")
            time.sleep(1)
            total_seconds -= 1
        print()  # Move to the next line after countdown
    except KeyboardInterrupt:
        print("\nTimer interrupted!")
        quit()

while True:
    get_aqi_function()
    countdown(1)  # 1-hour countdown

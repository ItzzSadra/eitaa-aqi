import time
import requests
from aqi_aqms import get_aqi
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def classify_aqi(aqi):
    if aqi <= 50:
        return "پاک", "🟢"
    elif 51 <= aqi <= 100:
        return "قابل قبول", "🟡"
    elif 101 <= aqi <= 150:
        return "ناسالم برای گروه های حساس", "🟠"
    elif 151 <= aqi <= 200:
        return "ناسالم", "🔴"
    elif 201 <= aqi <= 300:
        return "بسیار ناسالم", "🟣"
    else:
        return "خطرناک", "🟤"

def get_aqi_function():
    EITAA_API_KEY = os.getenv('EITAA_API_KEY')
    CHAT_ID = "10964115"

    # FIX: convert AQI to int
    aqi = int(get_aqi("اصفهان"))

    status, status_emoji = classify_aqi(aqi)

    current_time = datetime.now().strftime("%H:%M")
    print(current_time)

    data = f"""📊 شاخص آلودگی هوا
⏰ آمار ساعت : {current_time}
☁ شاخص: {aqi} {status} {status_emoji}
🪶@Esfahan_Tattili | اخبار مدارس اصفهان"""


    URL = f"https://eitaayar.ir/api/{EITAA_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={data}&date=0&parse_mode=&pin=off&viewCountForDelete="

    try:
        requests.get(URL)
    except:
        print("Error sending to Eitaa")

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
        print()
    except KeyboardInterrupt:
        print("\nTimer interrupted!")
        quit()

while True:
    get_aqi_function()
    countdown(1)

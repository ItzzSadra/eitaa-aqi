import time
import requests
from aqi import get_aqi

def my_function():
    print("\nRunning my function...")

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

while True:
    my_function()
    countdown(1)  # 1-hour countdown

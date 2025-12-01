from __future__ import annotations

import os
import time
import csv
from pathlib import Path
from datetime import datetime
from typing import Tuple

import requests
from dotenv import load_dotenv

from aqi_aqms import get_aqi


load_dotenv()

EITAA_API_KEY = os.getenv("EITAA_API_KEY")
CHAT_ID = "10379313"
DEFAULT_CITY = "اصفهان"
COUNTDOWN_HOURS = 1
REQUEST_TIMEOUT_SECONDS = 10

AQI_HISTORY_FILE = Path("aqi_history.csv")


def classify_aqi(aqi: int) -> Tuple[str, str]:
    """Return a human–readable AQI status (Persian) and an emoji."""
    if aqi <= 50:
        return "پاک", "🟢"
    if 51 <= aqi <= 100:
        return "قابل قبول", "🟡"
    if 101 <= aqi <= 150:
        return "ناسالم برای گروه های حساس", "🟠"
    if 151 <= aqi <= 200:
        return "ناسالم", "🔴"
    if 201 <= aqi <= 300:
        return "بسیار ناسالم", "🟣"
    return "خطرناک", "🟤"


def safe_get_aqi(city: str, max_retries: int = 5) -> int | None:
    """Get AQI for a city with retry logic and basic error handling."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Getting AQI for {city}... (try {attempt})")
            aqi_value = get_aqi(city)

            if aqi_value is None:
                raise ValueError("AQI is None")

            return int(aqi_value)

        except Exception as exc:
            print(f"Failed to get AQI: {exc}")
            time.sleep(3)

    print("❌ Could not retrieve AQI after multiple retries.")
    return None


def flow_detect(previous, now):
    if previous == now:
        return "بدون تغییر"
    if now > previous:
        return "افزایشی"
    if now < previous:
        return "کاهشی"


def flow_emoji_for(flow: str) -> str:
    if flow == "افزایشی":
        return "📈"
    if flow == "کاهشی":
        return "📉"
    return "➖"


def save_previous_aqi(aqi: int) -> None:
    """Save the current AQI to the CSV file."""
    with open(AQI_HISTORY_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["previous_aqi"])
        writer.writerow([aqi])


def load_previous_aqi() -> int | None:
    """Load previous AQI from the CSV file."""
    if not AQI_HISTORY_FILE.exists():
        return None

    try:
        with open(AQI_HISTORY_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            row = next(reader, None)
            if row:
                return int(row[0])
    except Exception:
        return None

    return None


def safe_request(url: str, max_retries: int = 5) -> bool:
    """Send a GET request with retries and timeout."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Sending message... (try {attempt})")
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            return True

        except Exception as exc:
            print(f"Failed to send message: {exc}")
            time.sleep(3)

    print("❌ Could not send message after retries.")
    return False


def send_aqi_message() -> None:
    """Fetch the AQI and send it to the configured Eitaa chat."""
    if not EITAA_API_KEY:
        print("❌ EITAA_API_KEY is not set. Aborting send.")
        return

    aqi = safe_get_aqi(DEFAULT_CITY)
    if aqi is None:
        print("Skipping message — AQI unavailable.")
        return

    # Load previous AQI
    previous_aqi = load_previous_aqi()

    # Detect flow
    if previous_aqi is None:
        flow = "بدون اطلاعات قبلی"
        flow_emoji = "➖"
    else:
        flow = flow_detect(previous_aqi, aqi)
        flow_emoji = flow_emoji_for(flow)

    # Save current AQI
    save_previous_aqi(aqi)

    # Status
    status, status_emoji = classify_aqi(aqi)
    current_time = datetime.now().strftime("%H:%M")

    message = (
        "📊 شاخص آلودگی هوا\n"
        f"⏰ آمار ساعت: {current_time}\n"
        f"☁ شاخص: {aqi} {status} {status_emoji}\n"
        f"{flow_emoji} روند: {flow}\n"
        "🪶@Esfahan_Tattili | اخبار مدارس اصفهان"
    )

    url = (
        f"https://eitaayar.ir/api/{EITAA_API_KEY}/sendMessage"
        f"?chat_id={CHAT_ID}"
        f"&text={message}"
        "&date=0&parse_mode=&pin=off&viewCountForDelete="
    )

    safe_request(url)


def countdown(hours: float = 1.0, bar_width: int = 30) -> None:
    """Display a countdown timer with a simple progress bar."""
    total_seconds = int(hours * 3600)
    elapsed = 0

    try:
        while elapsed < total_seconds:
            remaining = total_seconds - elapsed
            mins, secs = divmod(remaining, 60)
            hours_left, mins = divmod(mins, 60)
            timer = f"{hours_left:02d}:{mins:02d}:{secs:02d}"

            progress = elapsed / total_seconds if total_seconds else 1
            filled_length = int(bar_width * progress)
            bar = "█" * filled_length + "-" * (bar_width - filled_length)

            print(f"\rNext run in: {timer} [{bar}]", end="", flush=True)

            time.sleep(1)
            elapsed += 1

        print(f"\rNext run in: 00:00:00 [{'█' * bar_width}]", end="", flush=True)
        print()

    except KeyboardInterrupt:
        print("\nTimer interrupted by user.")
        raise SystemExit(0)


def main() -> None:
    """Main loop: send AQI message, then wait before next run."""
    while True:
        send_aqi_message()
        countdown(COUNTDOWN_HOURS)


if __name__ == "__main__":
    main()

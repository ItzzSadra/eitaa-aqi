import requests
from dotenv import load_dotenv
import os

load_dotenv()

CITY = "ّIsfahan"
API_KEY = os.getenv('API_KEY') # Because I'm gonna be sharing in github, I made sure the API Key wont be on there. I know its a free api but I dont care
URL = f"https://api.waqi.info/feed/{CITY}/"
response = requests.get(URL, params={"token": API_KEY}) # Looks Clean

# Check status
if response.status_code == 200:
    data = response.json()  # Convert JSON response to Python dict
    data = data['data']['aqi']
    print(data)
else:
    print(f"Error: {response.status_code}")

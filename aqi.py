import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_aqi(city: str) -> int | None:
    """
    Fetch the AQI (Air Quality Index) for a given city.
    
    Args:
        city (str): Name of the city.
        
    Returns:
        int | None: The AQI value if successful, None if there was an error.
    """
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        print("Error: API_KEY not found in environment variables.")
        return None

    URL = f"https://api.waqi.info/feed/{city}/"
    
    try:
        response = requests.get(URL, params={"token": API_KEY})
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx/5xx
        data = response.json()
        aqi = data['data']['aqi']
        return aqi
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except KeyError:
        print("Unexpected response structure.")
    
    return None

# Example usage
if __name__ == "__main__":
    city_aqi = get_aqi("Isfahan")
    if city_aqi is not None:
        print(f"AQI in Isfahan: {city_aqi}")

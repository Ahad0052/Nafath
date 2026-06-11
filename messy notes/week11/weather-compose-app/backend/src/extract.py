import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
# Keep the fallback city from .env just in case no city is provided
DEFAULT_CITY = os.getenv("CITY", "Muscat")

# 1. Update the function to accept a 'city' parameter with a default value
def extract_weather(city=None):
    
    # 2. Use the city passed from the frontend; if none passed, fall back to default
    search_city = city if city else DEFAULT_CITY

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={search_city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()
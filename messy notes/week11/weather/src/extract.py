import requests
import os
from dotenv import load_dotenv

api_key = os.getenv("API_KEY")
city = os.getenv("CITY")
def extract_weather():
    load_dotenv(override=True)

    

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    response.raise_for_status()
    return response.json()
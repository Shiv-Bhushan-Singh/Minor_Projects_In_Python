import os
import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"




def get_weather(city: str):

    if not API_KEY:
        raise ValueError("Weather API key is not configured.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise ConnectionError("Weather API request timed out.")

    except requests.exceptions.RequestException:
        raise ConnectionError("Unable to connect to weather service.")

    if response.status_code == 401:
        raise PermissionError("Invalid weather API key.")

    if response.status_code == 404:
        raise LookupError(f"City '{city}' was not found.")

    if response.status_code == 429:
        raise RuntimeError("Weather API rate limit exceeded.")

    if response.status_code >= 500:
        raise ConnectionError("Weather service is currently unavailable.")

    response.raise_for_status()

    data = response.json()

    weather = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"]
    }

    return weather




def get_forecast(city: str):

    if not API_KEY:
        raise ValueError("Weather API key is not configured.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise ConnectionError("Weather API request timed out.")

    except requests.exceptions.RequestException:
        raise ConnectionError("Unable to connect to weather service.")

    if response.status_code == 401:
        raise PermissionError("Invalid weather API key.")

    if response.status_code == 404:
        raise LookupError(f"City '{city}' was not found.")

    if response.status_code == 429:
        raise RuntimeError("Weather API rate limit exceeded.")

    if response.status_code >= 500:
        raise ConnectionError("Weather service is currently unavailable.")

    response.raise_for_status()

    data = response.json()

    forecast = []

    for item in data["list"]:

        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "feels_like": item["main"]["feels_like"],
            "humidity": item["main"]["humidity"],
            "pressure": item["main"]["pressure"],
            "wind_speed": item["wind"]["speed"],
            "condition": item["weather"][0]["main"],
            "description": item["weather"][0]["description"]
        })

    return {
        "city": data["city"]["name"],
        "country": data["city"]["country"],
        "forecast": forecast
    }


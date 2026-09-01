import os
import requests
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Get API key
API_KEY = os.getenv("API_KEY")


# OpenWeather API URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """
    Fetch current weather information for a city.
    """

    # Parameters for API request
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    # Send GET request
    response = requests.get(BASE_URL, params=params)

    # Raise an exception if API request failed
    response.raise_for_status()

    
    data = response.json()

    weather = { 
            
            "city": data["name"], 
            "country": data["sys"]["country"], "temperature": data["main"]["temp"], 
            "feels_like": data["main"]["feels_like"], 
            "humidity": data["main"]["humidity"], 
            "pressure": data["main"]["pressure"], 
            "wind_speed": data["wind"]["speed"], 
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"] 
            

            }
    return weather


# Test the function
if __name__ == "__main__":

    city = input("Enter city name: ")

    weather_data = get_weather(city) 
    print(weather_data)


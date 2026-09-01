import requests


BACKEND_URL = "http://127.0.0.1:8000"


def get_current_weather(city: str):

    response = requests.get(
        f"{BACKEND_URL}/weather/",
        params={"city": city},
        timeout=10
    )

    if response.status_code != 200:
        try:
            error = response.json()
            message = error.get(
                "detail",
                "Unable to fetch weather data."
            )
        except ValueError:
            message = "Unable to fetch weather data."

        raise Exception(message)

    return response.json()


def get_forecast(city: str):

    response = requests.get(
        f"{BACKEND_URL}/weather/forecast",
        params={"city": city},
        timeout=10
    )

    if response.status_code != 200:
        try:
            error = response.json()
            message = error.get(
                "detail",
                "Unable to fetch forecast data."
            )
        except ValueError:
            message = "Unable to fetch forecast data."

        raise Exception(message)

    return response.json()
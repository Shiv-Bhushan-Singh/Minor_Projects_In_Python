import requests
import streamlit as st

from api.weather_client import (
    get_current_weather,
    get_forecast
)

from components.current_weather import (
    display_current_weather
)

from components.forecast import (
    display_forecast,
    display_forecast_cards
)



st.set_page_config(
    page_title="Smart Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)


st.title("🌦️ Smart Weather Dashboard")

st.write(
    "Get current weather conditions and forecast information "
    "for any city."
)




city = st.text_input(
    "🔍 Search City",
    placeholder="Enter a city name, e.g. Delhi"
)


search_button = st.button(
    "Get Weather",
    type="primary"
)



if search_button:

    if not city.strip():

        st.warning(
            "Please enter a city name."
        )

    else:

        try:

            # Get current weather
            weather = get_current_weather(
                city.strip()
            )

            # Get forecast
            forecast = get_forecast(
                city.strip()
            )

            # Store data in session state
            st.session_state["weather"] = weather
            st.session_state["forecast"] = forecast

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the FastAPI backend."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The request timed out."
            )

        except Exception as e:

            st.error(
                f"❌ {str(e)}"
            )



if "weather" in st.session_state:

    weather = st.session_state["weather"]

    forecast = st.session_state["forecast"]

    display_current_weather(
        weather
    )

    st.divider()

    display_forecast(
        forecast
    )

    st.divider()

    display_forecast_cards(
        forecast
    )
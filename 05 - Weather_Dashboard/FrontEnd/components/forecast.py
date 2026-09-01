import pandas as pd
import plotly.express as px
import streamlit as st


def display_forecast(forecast_data):

    forecast = forecast_data["forecast"]

    # Convert forecast into DataFrame
    df = pd.DataFrame(forecast)

    # Convert datetime string into datetime object
    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    st.subheader("📈 Temperature Forecast")

    # Temperature chart
    fig = px.line(
        df,
        x="datetime",
        y="temperature",
        markers=True,
        labels={
            "datetime": "Time",
            "temperature": "Temperature (°C)"
        },
        title="Temperature Over Time"
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def display_forecast_cards(forecast_data):

    forecast = forecast_data["forecast"]

    df = pd.DataFrame(forecast)

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    # Extract date
    df["date"] = df["datetime"].dt.date

    # Get one forecast per day
    daily = (
        df.groupby("date")
        .first()
        .reset_index()
    )

    st.subheader("📅 Forecast")

    columns = st.columns(
        min(len(daily), 5)
    )

    for index, (_, row) in enumerate(
        daily.head(5).iterrows()
    ):

        with columns[index]:

            st.markdown(
                f"### {row['datetime'].strftime('%a')}"
            )

            condition = row["condition"]

            if condition == "Clear":
                icon = "☀️"

            elif condition == "Clouds":
                icon = "☁️"

            elif condition == "Rain":
                icon = "🌧️"

            elif condition == "Snow":
                icon = "❄️"

            elif condition == "Thunderstorm":
                icon = "⛈️"

            else:
                icon = "🌤️"

            st.markdown(
                f"# {icon}"
            )

            st.write(
                f"**{row['temperature']:.1f} °C**"
            )

            st.write(
                condition
            )

            st.write(
                f"💧 {row['humidity']}%"
            )

import streamlit as st


def display_current_weather(weather):

    st.subheader(
        f"📍 {weather['city']}, {weather['country']}"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🌡️ Temperature",
            f"{weather['temperature']:.1f} °C"
        )

    with col2:

        st.metric(
            "🤗 Feels Like",
            f"{weather['feels_like']:.1f} °C"
        )

    with col3:

        st.metric(
            "💧 Humidity",
            f"{weather['humidity']}%"
        )

    with col4:

        st.metric(
            "💨 Wind Speed",
            f"{weather['wind_speed']:.1f} m/s"
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write("☁️ **Condition**")
        st.write(
            weather["condition"]
        )

    with col2:

        st.write("📝 **Description**")
        st.write(
            weather["description"].capitalize()
        )

    with col3:

        st.write("🔵 **Pressure**")
        st.write(
            f"{weather['pressure']} hPa"
        )

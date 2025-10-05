import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Air Quality Forecast App", layout="wide")

# --- NOTICE ---
st.warning(
    "⚠️ Due to the current U.S. government shutdown, some NASA data services are temporarily unavailable. "
    "This demo uses sample air quality and weather data. Live integration will resume when services are restored."
)

# --- SAMPLE DATA (Simulating NASA / TEMPO / OpenAQ data) ---
data = {
    "City": ["Los Angeles", "New York", "Toronto", "Mexico City", "Vancouver", "Chicago", "Houston", "Miami"],
    "Lat": [34.0522, 40.7128, 43.65107, 19.4326, 49.2827, 41.8781, 29.7604, 25.7617],
    "Lon": [-118.2437, -74.0060, -79.347015, -99.1332, -123.1207, -87.6298, -95.3698, -80.1918],
    "AQI": [120, 90, 60, 150, 55, 100, 130, 70],
    "Forecast": [
        "Unhealthy for Sensitive Groups",
        "Moderate",
        "Good",
        "Unhealthy",
        "Good",
        "Unhealthy for Sensitive Groups",
        "Unhealthy",
        "Moderate"
    ],
    "Temp (°C)": [28, 23, 19, 25, 17, 20, 30, 29],
    "Humidity (%)": [30, 55, 60, 40, 70, 50, 65, 80]
}

df = pd.DataFrame(data)

# --- CITY DROPDOWN ---
selected_city = st.selectbox("🌆 Select a City", df["City"].unique())

# --- GET SELECTED CITY DATA ---
city_data = df[df["City"] == selected_city].iloc[0]

st.subheader(f"Air Quality & Weather Forecast for **{selected_city}**")
st.metric("Air Quality Index (AQI)", city_data["AQI"], "Based on sample data")
st.write(f"**Forecast:** {city_data['Forecast']}")
st.write(f"🌡️ Temperature: {city_data['Temp (°C)']} °C")
st.write(f"💧 Humidity: {city_data['Humidity (%)']} %")

# --- MAP ---
m = folium.Map(location=[city_data["Lat"], city_data["Lon"]], zoom_start=6)

# Add marker
popup_text = (
    f"{selected_city}<br>"
    f"AQI: {city_data['AQI']}<br>"
    f"Forecast: {city_data['Forecast']}"
)
folium.Marker(
    [city_data["Lat"], city_data["Lon"]],
    popup=popup_text,
    tooltip=selected_city,
    icon=folium.Icon(color="red" if city_data["AQI"] > 100 else "green")
).add_to(m)

# Show map
st_folium(m, width=700, height=500)

# --- FOOTER ---
st.caption("Data simulated due to NASA API downtime. Structure ready for live integration.")

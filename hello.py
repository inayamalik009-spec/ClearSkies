import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="ClearSkies 🌍", layout="wide")

# --- HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg",
        width=80
    )
with col2:
    st.title("🌍 ClearSkies")
    st.subheader("North America Air Quality & Weather Visualization Dashboard")

# --- NOTICE BANNER ---
st.warning(
    "⚠️ Due to the ongoing U.S. government shutdown, NASA data services (TEMPO, GIBS, Pandora) are temporarily unavailable. "
    "This demo uses sample datasets to showcase the app’s structure. Live data will be seamlessly integrated once services resume."
)

# --- INTRO SECTION ---
st.markdown(
    """
    ClearSkies integrates **NASA satellite data (TEMPO)** and **ground-based Pandora spectrometer data**  
    with local weather measurements to forecast and visualize **air quality across North America** in near real-time.

    🛰️ **TEMPO** → Large-scale NO₂ column data from orbit  
    🧪 **Pandora** → Local ground-based measurements for validation  
    🌡️ **Weather Data** → Temperature, humidity, wind for pollution dispersion context
    """
)

st.divider()

# --- SIDEBAR ---
st.sidebar.header("🧭 Controls")
st.sidebar.write("Customize your view and toggle data layers below.")

# Layer toggles
show_tempo = st.sidebar.checkbox("Show TEMPO Layer (Satellite)", value=True)
show_pandora = st.sidebar.checkbox("Show Pandora Stations (Ground)", value=True)

# --- SAMPLE DATA ---
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
    "Humidity (%)": [30, 55, 60, 40, 70, 50, 65, 80],
    "Wind (km/h)": [15, 20, 12, 10, 25, 18, 22, 16],
    "PM2.5 (µg/m³)": [45, 30, 12, 55, 10, 35, 60, 20]
}
df = pd.DataFrame(data)

# --- CITY DROPDOWN ---
selected_city = st.selectbox("🌆 Select a City", df["City"].unique())

# --- GET SELECTED CITY DATA ---
city_data = df[df["City"] == selected_city].iloc[0]

st.markdown(f"### 📊 Current Air Quality & Weather — **{selected_city}**")

# --- METRICS SECTION ---
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("AQI", city_data["AQI"], "Sample")
col_b.metric("Temperature (°C)", city_data["Temp (°C)"])
col_c.metric("Humidity (%)", city_data["Humidity (%)"])
col_d.metric("PM2.5", f"{city_data['PM2.5 (µg/m³)']} µg/m³")

st.info(f"**Forecast:** {city_data['Forecast']} | 💨 Wind Speed: {city_data['Wind (km/h)']} km/h")

# --- MAP ---
m = folium.Map(location=[city_data["Lat"], city_data["Lon"]], zoom_start=5, tiles="CartoDB positron")

# Selected city marker
aqi_color = "green"
if city_data["AQI"] > 150:
    aqi_color = "darkred"
elif city_data["AQI"] > 100:
    aqi_color = "red"
elif city_data["AQI"] > 50:
    aqi_color = "orange"

popup_text = (
    f"<b>{selected_city}</b><br>"
    f"AQI: {city_data['AQI']}<br>"
    f"Forecast: {city_data['Forecast']}<br>"
    f"Temp: {city_data['Temp (°C)']} °C<br>"
    f"PM2.5: {city_data['PM2.5 (µg/m³)']} µg/m³"
)

folium.Marker(
    [city_data["Lat"], city_data["Lon"]],
    popup=popup_text,
    tooltip=selected_city,
    icon=folium.Icon(color=aqi_color)
).add_to(m)

# --- TEMPO WMS LAYER (Satellite NO₂) ---
if show_tempo:
    tempo_layer_url = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
    try:
        folium.raster_layers.WmsTileLayer(
            url=tempo_layer_url,
            layers="OMI_NO2_Column_Amount",
            name="TEMPO NO₂ (Satellite)",
            format="image/png",
            transparent=True,
            attribution="NASA GIBS"
        ).add_to(m)
    except Exception:
        st.info("🌐 TEMPO layer unavailable (likely due to NASA service downtime).")

# --- PANDORA STATION POINTS (Sample) ---
if show_pandora:
    pandora_stations = [
        {"name": "Pandora Station - Los Angeles", "lat": 34.05, "lon": -118.25},
        {"name": "Pandora Station - New York", "lat": 40.71, "lon": -74.00},
        {"name": "Pandora Station - Toronto", "lat": 43.65, "lon": -79.38},
        {"name": "Pandora Station - Houston", "lat": 29.76, "lon": -95.36},
    ]
    for station in pandora_stations:
        folium.CircleMarker(
            location=[station["lat"], station["lon"]],
            radius=6,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.7,
            popup=station["name"],
        ).add_to(m)

# Layer control
folium.LayerControl(collapsed=False).add_to(m)

# Render map
st_folium(m, width=900, height=500)

# --- FOOTER ---
st.divider()
st.caption("🛰️ Built for NASA Space Apps Challenge 2025 | Data simulated due to NASA API downtime | TEMPO + Pandora structure ready for integration")

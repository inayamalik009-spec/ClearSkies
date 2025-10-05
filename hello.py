import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# --------------------------------------------
# Title and Description
# --------------------------------------------
st.set_page_config(page_title="ClearSkies - Air Quality App", layout="wide")
st.title("🌤️ ClearSkies: North American Air Quality Tracker")
st.write("This app integrates NASA & OpenAQ data to visualize and forecast air quality in major North American cities.")

# --------------------------------------------
# City List (Major North American cities)
# --------------------------------------------
CITIES = {
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "New York City": {"lat": 40.7128, "lon": -74.0060},
    "Toronto": {"lat": 43.6532, "lon": -79.3832},
    "Mexico City": {"lat": 19.4326, "lon": -99.1332},
    "Chicago": {"lat": 41.8781, "lon": -87.6298},
    "Vancouver": {"lat": 49.2827, "lon": -123.1207},
    "Houston": {"lat": 29.7604, "lon": -95.3698},
    "Montreal": {"lat": 45.5017, "lon": -73.5673},
    "Dallas": {"lat": 32.7767, "lon": -96.7970},
    "Miami": {"lat": 25.7617, "lon": -80.1918}
}

selected_city = st.selectbox("🌍 Select a city:", list(CITIES.keys()))

# --------------------------------------------
# OpenAQ API (v3) Setup
# --------------------------------------------
OPENAQ_API_KEY = st.secrets["OPENAQ_API_KEY"]

def get_air_quality_v3(city_name):
    url = "https://api.openaq.org/v3/measurements"
    headers = {"Authorization": f"Bearer {OPENAQ_API_KEY}"}
    params = {
        "city": city_name,
        "limit": 5,
        "sort": "desc",
        "order_by": "datetime"
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Error fetching air quality: {e}")
        return None

# --------------------------------------------
# Fetch and Display Air Quality Data
# --------------------------------------------
aq_data = get_air_quality_v3(selected_city)

st.subheader(f"🌡️ Air Quality in {selected_city}")

if aq_data and "results" in aq_data and len(aq_data["results"]) > 0:
    for m in aq_data["results"]:
        st.metric(
            label=f"{m['parameter'].upper()} ({m['unit']})",
            value=str(m['value']),
            help=f"Measured at {m['datetime']['utc']}"
        )
else:
    st.write("No recent air quality data available for this city.")

# --------------------------------------------
# Folium Map (Option 2: OpenStreetMap tiles)
# --------------------------------------------
coords = CITIES[selected_city]
m = folium.Map(location=[coords["lat"], coords["lon"]], zoom_start=7)

# Simple OSM tile layer (no WMS for now)
folium.TileLayer(
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attr="OpenStreetMap",
    name="OpenStreetMap",
    overlay=True
).add_to(m)

# City marker
folium.Marker(
    [coords["lat"], coords["lon"]],
    tooltip=selected_city,
    popup=f"Selected city: {selected_city}"
).add_to(m)

# Render map in Streamlit
st_folium(m, width=700, height=500)

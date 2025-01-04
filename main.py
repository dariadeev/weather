import streamlit as st, json, datetime as dt, pandas as pd
from app import default_location, unit_prefrences, save_jason, get_weather, date_time #favorite_location,
from datetime import datetime, timezone
import pytz
import matplotlib.pyplot as pltimport, numpy as np

st.title("Welcome to Weather Application")

settings_file = 'weather.json'
data = {}
with open(settings_file, 'w') as f:
        json.dump(data, f)

with open(settings_file) as f:
     data = json.load(f)

def_location = default_location()
# fav_location = favorite_location()
units = unit_prefrences()

data.update ({"default_location" : def_location})
data.update({"temperature_unit": units})

# unit_prefrences()
save_jason(settings_file, data)

# Default city name for weather app
city_name = data["default_location"]

# Get and display the weather for the entered city
response, temp_unit = get_weather(city_name, units)

# Check if the request was successful
if response.status_code == 200:
        # Parse the JSON response
        url_data = response.json()


        # Extract and display weather data
        des = url_data['days']
        current_temp = des[4].get('temp', 'No date available')
        humidity = url_data['currentConditions']['humidity']
        description = url_data["description"]
        tz = url_data["timezone"]



        # Print the weather information
        st.header(f"Weather for {city_name.title()}:")
        st.write(f"Time zone: {tz}")
        date_time(city_name, tz)
        st.write(f"Current Temperature: {current_temp}°{temp_unit}")
        st.write(f"Humidity: {humidity}%")
        st.write(f"description: {description}")

        # Extract weather and location data
        latitude = float(url_data.get('latitude', 0))  # Ensure we get latitude
        longitude = float(url_data.get('longitude', 0))  # Ensure we get longitude

        # Create a DataFrame for the map
        map_data = pd.DataFrame({
                'lat': [latitude],  # Wrap scalars in lists
                'lon': [longitude]  # Wrap scalars in lists
        })

        # Display the map
        st.subheader("Map Location:")
        st.map(map_data, color = [255, 0, 0])



else:
        st.write(f"Failed to fetch weather data for {city_name}. HTTP Status Code: {response.status_code}")





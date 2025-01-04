import streamlit as st, json,  pandas as pd, requests
import datetime as dt, pytz
from datetime import datetime, timezone
from app import default_location, unit_prefrences, save_jason, get_weather, date_time

import matplotlib.pyplot as plt

st.title("Welcome to Weather Application")

settings_file = 'weather.json'
data = {}
with open(settings_file, 'w') as f:
        json.dump(data, f)

with open(settings_file) as f:
     data = json.load(f)

def_location = default_location()
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
        st.write(f"Description: {description}")

# Prepare the data for plotting
        forecast = url_data.get('days', [])

        dates = [day['datetime'] for day in forecast]
        temps = [day['temp'] for day in forecast]
        humidity = [day['humidity'] for day in forecast]

        # Create a DataFrame for easy manipulation
        df = pd.DataFrame({
                'Date': pd.to_datetime(dates),
                f'Temperature {temp_unit}': temps,
                'Humidity (%)': humidity

        })

        # Plot the weather data
        # Temperature plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df["Date"], df[f'Temperature {temp_unit}'], marker='o', color='blue', label=f'Temperature {temp_unit}', alpha=0.6)
        ax.set_xlabel('Date')
        ax.set_ylabel(f'Temperature {temp_unit}')
        # ax.tick_params(axis='y', labelcolor='tab:red')
        ax.set_title(f"Weekly Weather Forecast for {city_name.title()}")

        # Feelslike plot
        ax2 = ax.twinx()
        ax2.plot(df['Date'], df['Humidity (%)'], marker='x', label='Humidity (%)', color='tab:orange')
        ax2.set_ylabel('Humidity (%)')
        # ax2.tick_params(axis='y', labelcolor='tab:blue')

        fig.tight_layout()
        st.pyplot(fig)

        # Extract location latitude and longitude
        latitude = float(url_data.get('latitude', 0))  # Ensure we get latitude
        longitude = float(url_data.get('longitude', 0))  # Ensure we get longitude

        # Create a DataFrame for the map
        map_data = pd.DataFrame({
                'lat': [latitude],  # Wrap scalars in lists
                'lon': [longitude]  # Wrap scalars in lists
        })

        # Display the map
        st.subheader(f"Map location of {city_name.title()}:")
        st.map(map_data, color = [255, 0, 0])

else:
        st.write(f"Failed to fetch weather data for {city_name}. HTTP Status Code: {response.status_code}")





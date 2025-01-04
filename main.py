import streamlit as st, json,  pandas as pd, requests
import datetime as dt, pytz
from datetime import datetime, timezone
from app import default_location, unit_prefrences, save_jason, get_weather, date_time
import numpy as np

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

#Compass view
        # Extract data for the wind
        days = url_data['days']
        wind_direction = days[0]['windspeed']  # Wind speed
        wind_degrees = days[0]['winddir'] # Wind direction in degrees

        # Create the compass plot for wind direction
        fig, ax = plt.subplots(figsize=(5, 5))  # Slightly larger figure for better clarity
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        st.subheader(f"Compass of Wind Speed and Direction:")
        # Display wind data to the side using columns
        col1, col2 = st.columns([1, 3])  # Creates two columns with different widths

        # Place the wind speed and direction information in the second column
        with col1:
                st.write("")  # Empty space to align content
        with col2:
                st.write(f"Wind Speed: {wind_direction} km/h")
                st.write(f"Wind Direction: {wind_degrees}°")

        # Plot the compass as a circle
        circle = plt.Circle((0, 0), 0.5, edgecolor='black', facecolor='white', lw=2)
        ax.add_artist(circle)

        # Plot arrows for each cardinal direction
        cardinal_directions = ['N', 'E', 'S', 'W']
        angle = np.linspace(0, 2 * np.pi, 4, endpoint=False)  # N, E, S, W
        for i, direction in enumerate(cardinal_directions):
                ax.text(np.cos(angle[i]) * 0.6, np.sin(angle[i]) * 0.6, direction, ha='center', va='center',
                        fontweight='bold', fontsize=12, color='black')  # Larger font size for better readability

        # Calculate wind direction arrow based on degrees
        angle_rad = np.deg2rad(wind_degrees)
        ax.arrow(0, 0, 0.3 * np.cos(angle_rad), 0.3 * np.sin(angle_rad), head_width=0.1, head_length=0.2, fc='blue',
                 ec='blue')

        # Customize plot appearance
        ax.set_aspect('equal', 'box')
        ax.axis('off')  # Turn off axis lines
        fig.tight_layout()  # Adjust layout to ensure everything fits

        # Display the plot
        st.pyplot(fig)

else:
        st.write(f"Failed to fetch weather data for {city_name}. HTTP Status Code: {response.status_code}")





import streamlit as st
import json
from app import default_location, unit_prefrences, save_jason, get_weather #favorite_location,


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

# Print the data
print(data)
st.write(data)

# Ask the user to enter a city name
# city_name = input("Enter the city name: ")
city_name = data["default_location"]

# Get and display the weather for the entered city
response = get_weather(city_name)

# Check if the request was successful
if response.status_code == 200:
        # Parse the JSON response
        url_data = response.json()
        # print(data)


        # Extract and display weather data
        current_temp = url_data['currentConditions']['temp']
        humidity = url_data['currentConditions']['humidity']
        description = url_data["description"]
        # description = data['days']
        # description = description[0].get('datetime', 'No date available')


        # Print the weather information
        st.write(f"Weather for {city_name}:")
        st.write(f"Current Temperature: {current_temp}°C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"description: {description}")


else:
        st.write(f"Failed to fetch weather data for {city_name}. HTTP Status Code: {response.status_code}")





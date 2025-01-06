import json, requests, streamlit as st
import datetime as dt, pytz
from datetime import datetime, timedelta


def date_time(city_name, diff_tz=None):
        # Get the current time in the specified timezone
        local_tz = pytz.timezone(diff_tz)

        now = datetime.now(local_tz)
        # Format the time
        difftime2 = now.strftime("%A, %B %d, %Y, %I:%M %p")
        diff_utc = now.strftime("%z")
        st.write(f"Date and time in {city_name}: {difftime2}, UTC is {diff_utc} (UK UTC is +0000)")

def selected_location(def_loc = 'Tel Aviv'):
    # Input a location
    new_location = st.text_input('Enter a location:').strip()

    if not new_location: # This checks if the string is empty
        st.write("Please select location for weather information, default location set to be Tel Aviv")
        return def_loc

    else: #If not empty

        return new_location


def unit_prefrences():

    units = st.radio('Pick your preference temperature units', ['Celsius', 'Fahrenheit']).strip()

    if not units:  # This checks if the string is empty
        return "Celsius"
    else:
        return units

# Function to get weather for a specified city
def get_weather(city_name, units):

    city_name = city_name

    # Define the URL for the Visual Crossing API
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}"

    temp_unit = "C"
    # Define the request parameters
    if units == 'Celsius':
        data_units = "metric"
    elif units == 'Fahrenheit':
        data_units ="us"
        temp_unit = "F"
    else:
        data_units ="sk"

    params = {
        "unitGroup": data_units,  # Use metric units (Celsius, km/h, etc.)
        "key": "CXHEHFTH24228RKB5W4WQ5SGH",  # Replace with your actual API key
    }
    # Send a GET request to the API
    response = requests.get(url, params=params)

    return response, temp_unit


def save_jason(settings_file, data):
    # Write the data to the file
    with open(settings_file, 'w') as f:
        json.dump(data, f)

    # Open the JSON file and load its contents
    with open(settings_file) as f:
        data = json.load(f)

    return
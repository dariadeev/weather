import json, requests, streamlit as st, datetime as dt
from datetime import datetime, timezone
import pytz

def date_time(city_name, diff_tz=None):
        # Get the current time in the specified timezone
        local_tz = pytz.timezone(diff_tz)

        now = datetime.now(local_tz)
        # Format the time
        difftime2 = now.strftime("%A, %B %d, %Y, %I:%M %p")
        st.write(f"Date and time in {city_name}: {difftime2}")

def default_location(def_location = 'Tel Aviv'):
    # Input a location
    new_location = st.text_input('Enter a location:').strip()

    if not new_location: # This checks if the string is empty
        st.write("No valid answer was provided, default location set to be Israel")
        return def_location

    else: #If not empty
        answer = st.selectbox('Do you want to save this as your default location?', ['yes', 'no']).strip()

        if answer == "yes":
            def_location = new_location
            return new_location
        elif answer == "no":
            return def_location
        else:
            st.write(f"No valid answer was provided, default location set to be {def_location}")
            return def_location

def unit_prefrences():

    units = st.radio('Pick your preference temperature units', ['Celsius', 'Fahrenheit']).strip()

    if not units:  # This checks if the string is empty
        return "Celsius"
    else:
        return units

# def favorite_location():
#     # Input multiple locations
#     locations = input("Enter a few locations separated by spaces: ").strip()
#     locations = locations.split()
#
#     if "favorite_locations" not in data:
#         data["favorite_locations"] = []
#
#     [data["favorite_locations"].append(loc.strip()) for loc in locations if loc.strip() and loc.strip() not in data["favorite_locations"]]
#
#     return

# Function to get weather for a specified city
def get_weather(city_name, units):
    # Encode the city name for use in the URL (e.g., spaces to %20)
    city_name = city_name

    # Define the URL for the Visual Crossing API
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}"

    # Define the request parameters
    if units == 'Celsius':
        data_units = "metric"
        temp_unit = "C"
    elif units == 'Fahrenheit':
        data_units ="us"
        temp_unit = "F"
    else:
        data_units ="sk"
        temp_unit = "C"

    params = {
        "unitGroup": data_units,  # Use metric units (Celsius, km/h, etc.)
        "key": "CXHEHFTH24228RKB5W4WQ5SGH",  # Replace with your actual API key
        "contentType": "json"  # Set content type to JSON
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
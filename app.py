import json
import requests
import streamlit as st

def default_location(def_location = 'Israel'):
    # Input a location
    # new_location = input(f"Enter a location: ").strip()
    new_location = st.text_input('Enter a location:').strip()

    if not new_location: # This checks if the string is empty
        print("No valid answer was provided, default location set to be Israel")
        return def_location

    else: #If not empty
        answer = st.text_input("Save this as the default location? (yes/no): ").strip().lower()

        if answer == "yes":
          return new_location
        elif answer == "no":
          return def_location
        else:
          print("No valid answer was provided, default location set to be Israel")
          return def_location

def unit_prefrences():
    units = st.text_input("Enter your preference setting for temperature units (Celsius or Fahrenheit): ").strip()

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
def get_weather(city_name):
    # Encode the city name for use in the URL (e.g., spaces to %20)
    city_name = city_name

    # Define the URL for the Visual Crossing API
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}"

    # Define the request parameters
    params = {
        "unitGroup": "metric",  # Use metric units (Celsius, km/h, etc.)
        "key": "CXHEHFTH24228RKB5W4WQ5SGH",  # Replace with your actual API key
        "contentType": "json"  # Set content type to JSON
    }

    # Send a GET request to the API
    response = requests.get(url, params=params)

    return response



def save_jason(settings_file, data):
    # Write the data to the file
    with open(settings_file, 'w') as f:
        json.dump(data, f)

    # Open the JSON file and load its contents
    with open(settings_file) as f:
        data = json.load(f)

    return
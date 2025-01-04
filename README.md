# Weather Application

## Description
The Weather Application is an interactive tool that provides weather updates for a user-specified location. Built using Python and Streamlit, the application fetches real-time weather data using an API and displays information such as temperature, humidity, description, and timezone.

The application also allows users to set a default location, choose between Celsius or Fahrenheit for temperature units, and save preferences persistently in a JSON file. Users can modify the settings directly within the app.

---

## Features
- Display real-time weather data for a specified city.
- Support for Celsius or Fahrenheit temperature units.
- Persistent storage of user preferences such as default location and temperature unit.
- Display of timezone and formatted local date and time.

---

## Installation and Usage

### Prerequisites
1. **Python 3.7 or later**  
   Ensure you have Python installed on your system. 
2. **Required Python packages**  
   Install the dependencies using the following command:
   ```bash
   pip install streamlit pytz requests

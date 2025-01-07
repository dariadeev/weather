import streamlit as st, json,  pandas as pd, numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from app import selected_location, unit_prefrences, save_jason, get_weather, date_time, dark_mode_on_off

st.title("Welcome to Weather Application")
settings_file = 'weather.json'
data = {}

with open(settings_file, 'w') as f:
        json.dump(data, f)

with open(settings_file) as f:
     data = json.load(f)

def main():

        location = selected_location()
        units = unit_prefrences()

        data.update ({"selected_location" : location})
        data.update({"temperature_unit": units})

        # Check if the user prefers dark mode
        dark_mode = dark_mode_on_off()

        # unit_prefrences()
        save_jason(settings_file, data)

        # Default city name for weather app
        city_name = data["selected_location"]

        # Get and display the weather for the entered city
        response, temp_unit = get_weather(city_name, units)

        # Check if the request was successful
        if response.status_code == 200:
                # Parse the JSON response
                url_data = response.json()
                forecast = url_data['days'] # Get all the days data from url_data

                # Extract and display weather data (current day)
                current_temp = url_data["currentConditions"]["temp"] # Current temperature
                feellike = url_data["currentConditions"]["feelslike"]  # feelslike temperature
                humidity = url_data['currentConditions']['humidity']   # humidity
                conditions = url_data['currentConditions']['conditions']
                description = url_data["description"]   #description of the weather
                tz = url_data["timezone"]  #time zone to extract date and time information

                # Print the weather information
                st.header(f"Weather for {
                city_name.title()}:")
                st.write(f"Time zone: {tz}")
                date_time(city_name, tz)
                st.write(f"Current Temperature: {current_temp}°{temp_unit}")
                st.write(f"Feels-like: {feellike}°{temp_unit}")
                st.write(f"Humidity: {humidity}%")
                st.write(f"Description: {conditions}, {description}")

        #### Temperature distribution
                st.subheader(f"Temperature distribution of {city_name.title()}:")

        #### Daily temp overview
                max_temps = [day['tempmax'] for day in forecast]
                min_temps = [day['tempmin'] for day in forecast]

                min_temp = min_temps[0]  # Minimum temperature
                max_temp = max_temps[0]  # Maximum temperature

                # Calculate thermometer width
                thermometer_width = max_temp - min_temp
                current_position = (current_temp - min_temp) / thermometer_width

                # Create a figure and axis
                fig, ax = plt.subplots(figsize=(10, 3))

                # Generate the gradient effect from -50°C to 50°C
                cmap = plt.get_cmap("coolwarm")
                norm = plt.Normalize(vmin=-50, vmax=50)

                # Define the temperature range
                temperature_range = np.linspace(-50, 50, 100)

                # Plot the gradient as a horizontal bar
                ax.barh(0, 100, left=0, color='white', height=0.3)

                # Draw the temperature range as a horizontal bar
                ax.plot([min_temp, max_temp], [0, 0], color='grey', linewidth=8, solid_capstyle='round',
                        label='Temperature Range')

                # Add the current temperature as a marker depending on the temp

                if current_temp >= 20 and temp_unit == 'C':
                        temp_color = 'red'
                elif current_temp >= 68 and temp_unit == 'F':
                        temp_color = 'red'
                else:
                        temp_color = 'blue'

                ax.scatter(current_temp, 0, color=temp_color, s=150, label='Current Temperature', zorder=5)

                # Annotate the current temperature marker
                ax.text(current_temp, 0.2, f'{current_temp}°{temp_unit}', color=temp_color, fontsize=10, ha='center', fontweight='bold')

                # Add labels for min and max temperatures
                ax.text(min_temp, -0.25, f'{min_temp}°{temp_unit}', color='black', fontsize=10, ha='center')
                ax.text(max_temp, -0.25, f'{max_temp}°{temp_unit}', color='black', fontsize=10, ha='center')

                # Customize the axis
                ax.set_xlim(min_temp - 5, max_temp + 5)
                ax.set_ylim(-1, 1)
                ax.axis('off')  # Hide axes for a cleaner look

                # Add title and legend
                ax.set_title(f'Daily Temperature Overview of {city_name.title()}', fontsize=17)
                ax.legend(loc='upper left', fontsize=10, frameon=False)

                # Show the plot
                plt.tight_layout()
                st.pyplot(fig)


        ### Weekly Weather Forecast
                # Prepare the data for plotting Weekly Weather Forecast

                # Today date
                today = datetime.now().date()
                dates = [datetime.strptime(day['datetime'], "%Y-%m-%d").date() for day in forecast]
                temps = [day['temp'] for day in forecast]
                humidity = [day['humidity'] for day in forecast]

                # Map dates to labels
                def date_to_label(date):
                        if date == today:
                                return "Today"
                        else:
                                return date.strftime("%a")  # Day name

                date_labels = [date_to_label(date) for date in dates]

                df = pd.DataFrame({
                        'Date': dates[:7],
                        'Date Label': date_labels[:7],
                        f'Temperature {temp_unit}': temps[:7],
                        'Humidity (%)': humidity[:7],
                })

                # Format today's date for the title
                formatted_date = today.strftime("%d.%m.%y")

                # Plot the weather data
                # Temperature plot
                fig, ax = plt.subplots(figsize=(8, 4))

                # Set background color based on dark mode preference
                if dark_mode == "On":
                        fig.patch.set_facecolor('black')
                        ax.set_facecolor('black')
                        title_color = 'white'
                        label_color = 'white'
                        grid_color = 'white'
                        tick_color = 'white'
                        plot_color = 'lightblue'
                else:
                        fig.patch.set_facecolor('white')
                        ax.set_facecolor('white')
                        title_color = 'black'
                        label_color = 'black'
                        grid_color = 'gray'
                        tick_color = 'black'
                        plot_color = 'blue'

                # Set grid and axis colors
                ax.grid(True, color=grid_color, linestyle='--', alpha=0.5)
                ax.tick_params(axis='both', colors=tick_color)  # Set tick color based on theme

                ax.plot(df["Date"], df[f'Temperature {temp_unit}'], marker='o', color='blue', label=f'Temperature {temp_unit}', alpha=0.6)
                ax.set_ylabel(f'Temperature {temp_unit}')
                ax.set_title(f"Weekly Weather Forecast for {formatted_date} {city_name.title()}", color=title_color)

                # Replace x-axis ticks with labels
                ax.set_xticks(df["Date"])
                ax.set_xticklabels(df["Date Label"], color=label_color)

                # Humidity plot
                ax2 = ax.twinx()
                ax2.plot(df['Date'], df['Humidity (%)'], marker='o', label='Humidity (%)', color='tab:orange')
                ax2.set_ylabel('Humidity (%)', color=label_color)

                # Set the grid and axis ticks to light color for the second axis
                ax2.tick_params(axis='both', colors=tick_color)  # Set tick color to white

                fig.tight_layout()
                st.pyplot(fig)

        ### Map Plot

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

# Run the main function
if __name__ == "__main__":
  main()


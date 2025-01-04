import streamlit as st
import json
from app import default_location, unit_prefrences, save_jason #favorite_location,


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
st.write("Hello ,let's learn how to build a streamlit app together")





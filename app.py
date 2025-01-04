import json

def default_location(def_location = 'Israel'):
    # Input a location
    new_location = input(f"Enter a location: ").strip()

    if not new_location: # This checks if the string is empty
        print("No valid answer was provided, default location set to be Israel")
        return def_location

    else: #If not empty
        answer = input("Save this as the default location? (yes/no): ").strip().lower()

        if answer == "yes":
          return new_location
        elif answer == "no":
          return def_location
        else:
          print("No valid answer was provided, default location set to be Israel")
          return def_location

def unit_prefrences():
    units = input("Enter your preference setting for temperature units (Celsius or Fahrenheit): ").strip()

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

def save_jason(settings_file, data):
    # Write the data to the file
    with open(settings_file, 'w') as f:
        json.dump(data, f)

    # Open the JSON file and load its contents
    with open(settings_file) as f:
        data = json.load(f)

    return
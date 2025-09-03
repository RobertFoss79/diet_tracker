from timestamp import date_time_format

# Define the unit of each measurement entered by the user
def parse_metrics(name, value, timestamp):
    if name == "weight":
        unit = "lbs"
    elif name == "fat":
        unit = "%"
    elif name == "BMI":
        unit = "%"
    elif name == "BMR":
        unit = "kcal/day"
    elif name == "visceral_fat":
        unit = ""
    elif name == "muscle":
        unit = "lbs"
    elif name == "bone_mass":
        unit = "lbs"
    elif name == "protein":
        unit = "%"
    elif name == "water":
        unit = "%"
    elif name == "skeletal_muscle":
        unit = "lbs"
    else:
        unit = "units" #Fallback for any future metrics
    # Return the values to be assigned to the dictionary
    return {
        "metric" : name,
        "value" : value,
        "unit" : unit,
        "timestamp" : timestamp, # Only need one date and time stamp per dictionary
    }



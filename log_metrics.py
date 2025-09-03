from parse_metrics import parse_metrics
from timestamp import date_time_format

# Collects user input for each metric during weekly weigh-in
# Generates a shared timestamp and returns a structured dictionary for each entry
def log_metrics():
    timestamp = date_time_format()
    weight = float(input("Enter your weight: "))
    fat = float(input("Enter your fat number: "))
    BMI = float(input("Enter your BMI: "))
    BMR = float(input("Enter your BMR: "))
    visceral_fat = float(input("Enter your visceral fat: "))
    muscle = float(input("Enter your muscle: "))
    bone_mass = float(input("Enter your bone mass: "))
    protein = float(input("Enter your protein: "))
    water = float(input("Enter your water: "))
    skeletal_muscle = float(input("Enter your skeletal muscle: "))

    # Build as dict-of-dicts, then return as list-of-dicts
    metrics = {
        "weight": parse_metrics("weight", weight, timestamp),
        "fat": parse_metrics("fat", fat, timestamp),
        "BMI": parse_metrics("BMI", BMI, timestamp),
        "BMR": parse_metrics("BMR", BMR, timestamp),
        "visceral_fat": parse_metrics("visceral_fat", visceral_fat, timestamp),
        "muscle": parse_metrics("muscle", muscle, timestamp),
        "bone_mass": parse_metrics("bone_mass", bone_mass, timestamp),
        "protein": parse_metrics("protein", protein, timestamp),
        "water": parse_metrics("water", water, timestamp),
        "skeletal_muscle": parse_metrics("skeletal_muscle", skeletal_muscle, timestamp),
    }

    return list(metrics.values())  # Returns a list of dicts

from timestamp import date_time_format
from csv_utils import save_to_csv

def log_activity():
    """
    Prompt user to log physical activity with duration, calories, and optional distance.
    Returns a list of dicts for CSV logging.
    """
    print("\n🏃 Log Physical Activity")
    entries = []

    while True:
        activity_type = input("Activity type (e.g., walk, resistance training, mowing): ").strip()
        if not activity_type:
            print("Activity type cannot be empty. Please enter a value.")
            continue

        try:
            duration = float(input("Duration in minutes: ").strip())
            calories = float(input("Calories burned: ").strip())
            distance = input("Distance in miles (optional, press Enter to skip): ").strip()
            distance = float(distance) if distance else ""
        except ValueError:
            print("Invalid input. Please enter numeric values for duration, calories, and distance.")
            continue

        notes = input("Notes (optional): ").strip()
        timestamp = date_time_format()

        entry = {
            "timestamp": timestamp,
            "activity_type": activity_type,
            "duration_minutes": duration,
            "calories_burned": calories,
            "distance_miles": distance,
            "notes": notes
        }

        entries.append(entry)
        print("✔️ Entry added.\n")

        more = input("Log another activity? (y/n): ").strip().lower()
        if more != 'y':
            break

    return entries

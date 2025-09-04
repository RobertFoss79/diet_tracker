from timestamp import date_time_format
from csv_utils import save_to_csv

def log_food():
    """
    Prompt user to log food intake with calories and protein.
    Returns a list of dicts for CSV logging.
    """
    print("\n🍽️ Log Food Intake")
    entries = []

    while True:
        food = input("Food item (or 'done' to finish): ").strip()
        if food.lower() == "done":
            break

        calories = input("Calories: ").strip()
        protein = input("Protein (g): ").strip()
        notes = input("Notes (optional): ").strip()
        timestamp = date_time_format()

        entry = {
            "timestamp": timestamp,
            "food": food,
            "calories": calories,
            "protein": protein,
            "notes": notes
        }

        entries.append(entry)
        print("✔️ Entry added.\n")

    return entries

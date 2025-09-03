from log_metrics import log_metrics
# from log_food import log_food        # To be added later
# from log_activity import log_activity  # To be added later
from csv_utils import load_existing_csv, save_to_csv

def main():
    while True:
        print("\n📊 Diet Tracker")
        print("1. Log Weekly Metrics")
        print("2. Log Food Intake")
        print("3. Log Physical Activity")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            # METRICS LOGGING
            load_existing_csv("metrics_log.csv")  # Load existing file if present (for continuity)
            new_data_list = log_metrics()         # Get new metrics from user (list of dicts)
            save_to_csv("metrics_log.csv", new_data_list)

        elif choice == "2":
            # FOOD LOGGING (placeholder)
            load_existing_csv("food_log.csv")
            print("Food logging not yet implemented.")

        elif choice == "3":
            # ACTIVITY LOGGING (placeholder)
            load_existing_csv("activity_log.csv")
            print("Activity logging not yet implemented.")

        elif choice == "4":
            print("Exiting. Stay compliant, stay kind.")
            break

        else:
            print("Invalid choice. Please select 1–4.")

if __name__ == "__main__":
    main()
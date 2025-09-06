from log_metrics import log_metrics
from log_food import log_food
from log_activity import log_activity
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
            load_existing_csv("metrics_log.csv")
            new_data_list = log_metrics()
            new_data_list.sort(key=lambda x: x['timestamp'])  # ⬅️ Sort by timestamp
            save_to_csv("metrics_log.csv", new_data_list)

        elif choice == "2":
            # Food Logging
            new_data_list = log_food()
            new_data_list.sort(key=lambda x: x['timestamp'])  # ⬅️ Sort by timestamp
            save_to_csv("food_log.csv", new_data_list)



        elif choice == "3":
            # Activity Logging
            activity_entries = log_activity()
            activity_entries.sort(key=lambda x: x['timestamp'])
            save_to_csv('activity_log.csv', activity_entries)


        elif choice == "4":
            print("Exiting. Stay compliant, stay kind.")
            break

        else:
            print("Invalid choice. Please select 1–4.")

if __name__ == "__main__":
    main()
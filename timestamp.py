from datetime import datetime

# Define the time stamp, either a custom time stamp, or the current date and time if nothing entered.
def get_timestamp(custom_input=None):
    if custom_input:
        return custom_input
    else:
        return datetime.now().strftime("%m-%d-%Y %H:%M")
    
# Ask the user if they want to enter a custom date and time.
def date_time_format():
    while True:
        choice = input("Do you want to enter a custom date and time? y/n: ").strip().lower()
        if choice == "y":
            custom = input("Enter date and time (MM-DD-YYYY HH:MM): ").strip()
            try:
                datetime.strptime(custom, "%m-%d-%Y %H:%M")
                return custom
            except ValueError:
                print("Invalid format. Please use MM-DD-YYYY HH:MM.")
        elif choice == "n":
            return datetime.now().strftime("%m-%d-%Y %H:%M")
        else:
            print("Please enter 'y' or 'n'")
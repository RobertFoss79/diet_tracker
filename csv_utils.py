import os
import csv

def csv_exists(filename):
    """
    Check if a CSV file already exists in the filesystem.

    Args:
        filename (str): The name or path of the CSV file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(filename)


def load_existing_csv(filename):
    """
    Load existing CSV rows into a list of dictionaries.

    Each row in the CSV becomes a dictionary where keys are column headers
    and values are the row's data. If the file doesn't exist, an empty list
    is returned and a message is printed.

    Args:
        filename (str): The name or path of the CSV file.

    Returns:
        list[dict]: A list of dictionaries representing the CSV rows.
    """
    data = []
    if csv_exists(filename):
        # Open the file in read mode, ensuring newline handling is consistent
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)  # Reads rows as dicts keyed by header
            for row in reader:
                data.append(row)
    else:
        # Let the user know a new file will be created when saving
        print(f"No existing file found for {filename}. A new one will be created.")
    return data


def save_to_csv(filename, data):
    """
    Append new rows to a CSV file, creating it if needed.
    Inserts a blank row after each batch for visual separation.
    """
    if not data:
        print("No data to save.")
        return

    fieldnames = list(data[0].keys())
    file_exists = csv_exists(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for entry in data:
            writer.writerow(entry)

        # Add a blank row for separation
        writer.writerow({field: "" for field in fieldnames})

    print(f"Data saved to {filename}")


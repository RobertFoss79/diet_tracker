import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

def load_metrics(filename="metrics_log.csv"):
    """
    Load long-format metrics CSV and group entries by timestamp.
    Returns a list of dicts, each representing a full snapshot.
    """
    snapshots = defaultdict(dict)

    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ts_str = row.get("timestamp")
            metric = row.get("metric")
            value = row.get("value")

            if not ts_str or not metric or not value:
                continue

            try:
                ts = datetime.strptime(ts_str.strip(), "%m-%d-%Y %H:%M")
                val = float(value.strip())
                snapshots[ts][metric] = val
            except ValueError:
                continue  # Skip malformed rows

    # Convert to list of dicts with timestamp included
    return [{"timestamp": ts, **metrics} for ts, metrics in sorted(snapshots.items())]

def summarize_metric(data, metric):
    """
    Print total and percent change for a given metric across time.
    """
    values = [(entry["timestamp"], entry.get(metric)) for entry in data if metric in entry]
    values = [(ts, val) for ts, val in values if isinstance(val, (int, float))]

    if len(values) < 2:
        print(f"Not enough valid data for {metric}")
        return

    start_ts, start_val = values[0]
    end_ts, end_val = values[-1]
    delta = end_val - start_val
    percent = (delta / start_val) * 100 if start_val else 0

    print(f"\n📊 {metric.capitalize()} Summary:")
    print(f"{start_ts.strftime('%m-%d-%Y')} → {end_ts.strftime('%m-%d-%Y')}")
    print(f"Start: {start_val:.2f}, End: {end_val:.2f}")
    print(f"Change: {delta:+.2f} ({percent:+.2f}%)")

def get_date_input(prompt):
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%m-%d-%Y")
    except ValueError:
        print("Invalid format. Use MM-DD-YYYY.")
        return get_date_input(prompt)

def summarize_rolling_weight(data):
    """
    Outputs rolling 7-day weight change summaries.
    """
    weight_entries = [entry for entry in data if "weight" in entry]
    if len(weight_entries) < 2:
        print("\nNot enough weight data for rolling summary.")
        return

    print("\n📆 Rolling 7-Day Weight Change:")
    for i in range(len(weight_entries) - 1):
        start = weight_entries[i]
        end = weight_entries[i + 1]
        days = (end["timestamp"] - start["timestamp"]).days

        if days < 7:
            continue  # Skip if not a full week

        delta = end["weight"] - start["weight"]
        percent = (delta / start["weight"]) * 100 if start["weight"] else 0

        print(f"{start['timestamp'].strftime('%m-%d')} → {end['timestamp'].strftime('%m-%d')}: "
              f"{delta:+.2f} lbs ({percent:+.2f}%) over {days} days")
        
def export_summary_to_csv(data, filename="metrics_summary_output.csv"):
    """
    Export summary data to a CSV file for Calc with clean section headers.
    """
    metrics = ["weight", "fat", "muscle", "water", "BMI", "BMR", "visceral_fat", "bone_mass", "protein", "skeletal_muscle"]
    weight_entries = [entry for entry in data if "weight" in entry]
    rows = []

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Section 1: Total Change Summary
        writer.writerow(["# Total Change Summary"])
        writer.writerow(["metric", "start_date", "start_value", "end_date", "end_value", "delta", "percent_change"])
        for metric in metrics:
            values = [(entry["timestamp"], entry.get(metric)) for entry in data if metric in entry]
            values = [(ts, val) for ts, val in values if isinstance(val, (int, float))]
            if len(values) < 2:
                continue
            start_ts, start_val = values[0]
            end_ts, end_val = values[-1]
            delta = end_val - start_val
            percent = (delta / start_val) * 100 if start_val else 0
            writer.writerow([
                metric,
                start_ts.strftime("%m-%d-%Y"),
                f"{start_val:.2f}",
                end_ts.strftime("%m-%d-%Y"),
                f"{end_val:.2f}",
                f"{delta:+.2f}",
                f"{percent:+.2f}"
            ])

        # Section 2: Average Weight Change
        if len(weight_entries) >= 2:
            writer.writerow([])
            writer.writerow(["# Average Weight Change"])
            writer.writerow(["avg_weekly", "avg_daily", "weeks", "days"])
            start = weight_entries[0]
            end = weight_entries[-1]
            days = (end["timestamp"] - start["timestamp"]).days
            weeks = days / 7 if days >= 7 else 1
            delta = end["weight"] - start["weight"]
            avg_weekly = delta / weeks
            avg_daily = delta / days if days > 0 else delta
            writer.writerow([
                f"{avg_weekly:+.2f}",
                f"{avg_daily:+.2f}",
                f"{weeks:.1f}",
                f"{days}"
            ])

        # Section 3: Rolling 7-Day Weight Change
        writer.writerow([])
        writer.writerow(["# Rolling 7-Day Weight Change"])
        writer.writerow(["start_date", "end_date", "delta", "percent_change", "days"])
        for i in range(len(weight_entries) - 1):
            start = weight_entries[i]
            end = weight_entries[i + 1]
            days = (end["timestamp"] - start["timestamp"]).days
            if days < 7:
                continue
            delta = end["weight"] - start["weight"]
            percent = (delta / start["weight"]) * 100 if start["weight"] else 0
            writer.writerow([
                start["timestamp"].strftime("%m-%d-%Y"),
                end["timestamp"].strftime("%m-%d-%Y"),
                f"{delta:+.2f}",
                f"{percent:+.2f}",
                f"{days}"
            ])

        # Section 4: Milestone Crossings
        writer.writerow([])
        writer.writerow(["# Milestone Crossings"])
        writer.writerow(["milestone", "crossed_on", "weight"])
        weight_values = [entry["weight"] for entry in weight_entries]
        if weight_values:
            milestones = [w for w in range(260, int(min(weight_values)) - 1, -10)]
            for m in milestones:
                for entry in weight_entries:
                    if entry["weight"] <= m:
                        writer.writerow([
                            f"{m}",
                            entry["timestamp"].strftime("%m-%d-%Y"),
                            f"{entry['weight']:.2f}"
                        ])
                        break

    print(f"\n📁 Exported summary to {filename}")


def run_summary():
    data = load_metrics()
    print(f"\n✅ Loaded {len(data)} snapshots from metrics_log.csv")

    # Prompt for optional date range
    print("\n📅 Optional Date Range Filter")
    start_date = get_date_input("Start date (MM-DD-YYYY) or press Enter to skip: ")
    end_date = get_date_input("End date (MM-DD-YYYY) or press Enter to skip: ")
    if end_date:
        end_date = end_date.replace(hour=23, minute=59)

    # Filter data by date range
    filtered = [
        entry for entry in data
        if (not start_date or entry["timestamp"] >= start_date) and
           (not end_date or entry["timestamp"] <= end_date)
    ]

    print(f"\n📊 Summary for {len(filtered)} snapshots")
    for metric in ["weight", "fat", "muscle", "water", "BMI", "BMR", "visceral_fat", "bone_mass", "protein", "skeletal_muscle"]:
        summarize_metric(filtered, metric)

    # Weekly and daily average weight change
    weight_entries = [entry for entry in filtered if "weight" in entry]
    if len(weight_entries) >= 2:
        start = weight_entries[0]
        end = weight_entries[-1]
        days = (end["timestamp"] - start["timestamp"]).days
        weeks = days / 7 if days >= 7 else 1
        delta = end["weight"] - start["weight"]
        avg_weekly = delta / weeks
        avg_daily = delta / days if days > 0 else delta

        print(f"\n📉 Average Weekly Weight Change: {avg_weekly:+.2f} lbs/week over {weeks:.1f} weeks")
        print(f"📈 Average Daily Weight Change:  {avg_daily:+.2f} lbs/day over {days} days")

    summarize_rolling_weight(filtered)
    launch_dashboard(filtered)
    export_summary_to_csv(filtered)

def launch_dashboard(data):
    """
    Visual dashboard: weight over time, milestones, rolling changes.
    """
    if len(data) < 2 or "weight" not in data[0]:
        print("\nNot enough data for dashboard.")
        return

    # Extract timestamps and weights
    timestamps = [entry["timestamp"] for entry in data if "weight" in entry]
    weights = [entry["weight"] for entry in data if "weight" in entry]

    # Plot weight over time
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, weights, marker='o', label="Weight", color="blue")

    # Milestone markers (every 10 lbs from 260 down)
    milestones = [w for w in range(260, int(min(weights)) - 1, -10)]
    for m in milestones:
        for i, wt in enumerate(weights):
            if wt <= m:
                plt.axhline(y=m, color='green', linestyle='--', alpha=0.3)
                plt.text(timestamps[i], m, f"{m} lbs", color='green', fontsize=8)
                break

    # Rolling 7-day weight change bars
    for i in range(len(weights) - 1):
        days = (timestamps[i + 1] - timestamps[i]).days
        if days >= 7:
            delta = weights[i + 1] - weights[i]
            mid_ts = timestamps[i] + (timestamps[i + 1] - timestamps[i]) / 2
            plt.bar(mid_ts, delta, width=3, color='orange', alpha=0.5)

    # Labels and layout
    plt.title("📊 Weight Progress Dashboard")
    plt.xlabel("Date")
    plt.ylabel("Weight (lbs)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    run_summary()

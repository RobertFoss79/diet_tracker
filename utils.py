# utils.py - Analytical Functions

from datetime import date
from itertools import groupby

# --- DAILY SUMMARY CALCULATIONS ---

def calculate_daily_summary(food_entries, activity_entries, weighin_entries):
    """
    Calculates the total macros and Calorie Deficit/Surplus for a list of entries,
    incorporating BMR from the weigh-ins.
    """
    daily_summary = {}

    # Map BMRs to dates (We use the most recent BMR if one isn't logged for a specific day)
    bmr_lookup = {}
    if weighin_entries:
        # Sort weigh-ins oldest first to allow BMR tracking to use the most recent value
        weighin_entries.sort(key=lambda x: x.date_logged)
        
        # Track the last recorded BMR to fill in gaps
        last_bmr = 0
        
        for entry in weighin_entries:
            last_bmr = entry.bmr_kcal # BMR is BMR kcal/day
            bmr_lookup[entry.date_logged.strftime('%Y-%m-%d')] = last_bmr

    # --- Step 1 & 2: Aggregate Food and Activity ---
    
    # 1. Process Food Entries (Calories Consumed, Macros)
    all_dates = set(e.date_eaten.strftime('%Y-%m-%d') for e in food_entries)
    all_dates.update(e.date_logged.strftime('%Y-%m-%d') for e in activity_entries)

    for day_str in all_dates:
        daily_summary[day_str] = {
            "calories_consumed": sum(e.calories for e in food_entries if e.date_eaten.strftime('%Y-%m-%d') == day_str),
            "protein_consumed": sum(e.protein for e in food_entries if e.date_eaten.strftime('%Y-%m-%d') == day_str),
            "carbs_consumed": sum(e.carbs for e in food_entries if e.date_eaten.strftime('%Y-%m-%d') == day_str),
            "fat_consumed": sum(e.fat for e in food_entries if e.date_eaten.strftime('%Y-%m-%d') == day_str),
            "calories_burned": sum(e.calories_burned for e in activity_entries if e.date_logged.strftime('%Y-%m-%d') == day_str),
            "bmr": bmr_lookup.get(day_str, 0), # Get BMR if available for that day
            "total_expenditure": 0, # Placeholder for BMR + Activity
            "cal_deficit_surplus": 0, # The final calculated value
        }

    # --- Step 3: Calculate Final Deficit/Surplus ---
    # Deficit/Surplus = Consumed - (BMR + Activity Burned)
    for day_data in daily_summary.values():
        
        # If BMR wasn't found for the specific log date, try to estimate a close BMR
        if day_data["bmr"] == 0 and weighin_entries:
             # Use the BMR from the LATEST weigh-in as a reasonable estimate if the daily BMR is missing
             day_data["bmr"] = weighin_entries[-1].bmr_kcal 
        
        day_data["total_expenditure"] = day_data["bmr"] + day_data["calories_burned"]
        
        # Calculate Deficit/Surplus
        day_data["cal_deficit_surplus"] = day_data["calories_consumed"] - day_data["total_expenditure"]
        
    final_list = [dict(date=k, **v) for k, v in daily_summary.items()]
    final_list.sort(key=lambda x: x['date'], reverse=True)
    
    return final_list

# --- METRIC TREND CALCULATIONS ---

def analyze_metric_trends(weighin_entries):
    """
    Analyzes historical WeighIn data to determine overall trends for each BeWell metric.
    """
    if not weighin_entries or len(weighin_entries) < 2:
        return {} 

    weighin_entries.sort(key=lambda x: x.date_logged)
    
    latest_entry = weighin_entries[-1]
    oldest_entry = weighin_entries[0]

    metric_map = {
        'weight_lbs': {'label': 'Weight', 'unit': 'lbs'},
        'fat_pct': {'label': 'Body Fat', 'unit': '%'},
        'bmi': {'label': 'BMI', 'unit': ''},
        'bmr_kcal': {'label': 'BMR', 'unit': 'kcal/day'},
        'visceral_fat': {'label': 'Visceral Fat', 'unit': ''},
        'muscle_lbs': {'label': 'Muscle', 'unit': 'lbs'},
        'bone_mass_lbs': {'label': 'Bone Mass', 'unit': 'lbs'},
        'protein_pct': {'label': 'Protein', 'unit': '%'},
        'water_pct': {'label': 'Water', 'unit': '%'},
        'skeletal_muscle_lbs': {'label': 'Skeletal Muscle', 'unit': 'lbs'},
    }
    
    trend_summary = {}

    for col, info in metric_map.items():
        latest_value = getattr(latest_entry, col)
        oldest_value = getattr(oldest_entry, col)
        change = latest_value - oldest_value

        trend_summary[col] = {
            'label': info['label'],
            'unit': info['unit'],
            'latest_value': latest_value,
            'oldest_value': oldest_value,
            'change': change,
            'trend': 'Gain' if change > 0 else 'Loss' if change < 0 else 'No Change'
        }
        
    return trend_summary
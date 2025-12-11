# 🥗 Diet Tracker: Comprehensive Health Logging Application

This is a Flask-based diet and fitness logging application designed to replace the user's previous set of command-line interface (CLI) scripts with a modern, integrated web interface. It provides comprehensive tracking for food, physical activity, and detailed body metrics, along with an integrated summary and analysis page.

The application uses **Flask**, **Flask-SQLAlchemy** for database management, and **Flask-Migrate** for robust database version control.

## 💾 Database Models & Persistence

The application uses four distinct database models to manage data integrity:

| Model Name | Purpose | Key Fields | Persistence Feature |
| :--- | :--- | :--- | :--- |
| `FoodItem` | **Permanent Dictionary** of food/recipes. | Name, Calories, Protein, Carbs, Fat (per serving) | Ensures macro data is consistent and reusable. |
| `FoodEntry` | **Daily Log** of food consumption. | Date, `FoodItem` ID, **Serving Multiplier**, Calculated Macros | Calculates final macros based on user-entered serving size. |
| `ActivityEntry` | **Daily Log** of exercise. | Date, Activity Type, Duration, Calories Burned, Distance | Tracks energy expenditure. |
| `WeighIn` | **Body Metrics** from BeWell scale. | Date, **10 specific BeWell metric fields** (Weight, Fat%, BMR, Muscle, etc.) | Provides complex historical data for trend analysis. |

## 🚀 Application Functionality

### 1. Food Logging (`/` and `/manage_food`)

* **Food Dictionary Management:** Allows the user to add, view, and update Food Items/Recipes (e.g., "93/7 Ground Beef") in a centralized, persistent dictionary.
* **Daily Logging:** Users select an item from the dictionary, enter the **Serving Multiplier**, and the application accurately calculates and logs the total calories and macros for that entry.

### 2. Activity Logging (`/log/activity`)

* Allows users to log workouts by activity type, duration, and estimated calories burned, replacing the old `log_activity.py` script.

### 3. Metrics Logging (`/log/metrics`)

* Allows the user to log all **10 fields** tracked by their BeWell body composition scale in a single entry, focusing on objective progress metrics (excluding subjective scores like Body Age).

### 4. Summary and Analysis (`/summary`)

This page provides the core analytical functionality requested:

* **Calorie Deficit/Surplus Calculation:** The central calculation shows the daily energy balance using the accurate formula:
    $$\text{Deficit/Surplus} = (\text{Total Food Consumed}) - (\text{BMR} + \text{Activity Burned})$$
    The required BMR is pulled from the latest `WeighIn` metric entry to provide a robust daily analysis.
* **Body Metric Trends:** Compares the user's latest `WeighIn` data against the oldest `WeighIn` data to calculate the overall change (gain/loss) for all 10 metrics. *Note: Requires at least two entries to display trends.*

### 5. History and Filtering (`/history`)

* Allows the user to filter and view past food log entries by a specific date range, providing necessary historical log access for detailed review.

## 💻 Setup and Installation

1.  **Install Dependencies:**
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Migrate
    ```
    *(If using a requirements.txt file, use: `pip install -r requirements.txt`)*

2.  **Initialize Database Migration Repository:** (Run once)
    ```bash
    flask db init
    ```

3.  **Create and Apply Initial Database Structure:** (Creates the `site.db` file)
    ```bash
    flask db migrate -m "Initial models setup"
    flask db upgrade
    ```

4.  **Run the Application:**
    ```bash
    python app.py
    ```

5.  **Access:** Open your web browser and navigate to `http://127.0.0.1:5000/`.

---
*Created as a final project submission for CS50x.*
# app.py - The Core Flask Application

# Import necessary modules from Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from utils import calculate_daily_summary, analyze_metric_trends

# --- FLASK APPLICATION SETUP ---
app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# --- DATABASE MIGRATION SETUP (NEW) ---
# Initialize Flask-Migrate, linking the Flask app and the SQLAlchemy database
# This allows the 'flask db' commands to work
migrate = Migrate(app, db)

# --- DATABASE MODELS (The 'M' in MVC) ---
# NOTE: We use db.Date for date-only fields as requested.

# 1. FoodItem Model (The permanent Food Dictionary/Recipe Book)
class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    
    # Macros per serving
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False, default=0)
    carbs = db.Column(db.Float, nullable=False, default=0) 
    fat = db.Column(db.Float, nullable=False, default=0)

    # Relationship: Allows us to see all FoodEntry logs for this specific FoodItem
    entries = db.relationship('FoodEntry', backref='source_food', lazy=True)

    def __repr__(self):
        return f"FoodItem('{self.name}', {self.calories} cal)"

# 2. FoodEntry Model (Tracks daily consumption - links to FoodItem)
class FoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key linking to the FoodItem dictionary
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_item.id'), nullable=False) 
    
    # Data stored in the log (Calculated based on multiplier)
    food_name = db.Column(db.String(100), nullable=False) 
    
    # NEW: Store the multiplier used for this entry
    serving_multiplier = db.Column(db.Float, default=1.0) 
    
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, default=0)
    carbs = db.Column(db.Float, default=0) 
    fat = db.Column(db.Float, default=0)
    
    notes = db.Column(db.Text, default="")
    date_eaten = db.Column(db.Date, nullable=False, default=date.today) 

    def __repr__(self):
        return f"FoodEntry('{self.date_eaten}', '{self.food_name}', {self.calories} cal)"


# 3. ActivityEntry Model (Tracks physical activity/calories burned)
class ActivityEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(100), nullable=False) 
    duration_minutes = db.Column(db.Float, nullable=False)   
    calories_burned = db.Column(db.Integer, nullable=False)  
    distance_miles = db.Column(db.Float, default=0)          
    notes = db.Column(db.Text, default="")
    date_logged = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f"ActivityEntry('{self.date_logged}', '{self.activity_type}', {self.calories_burned} cal burned)"

# 4. WeighIn Model (Tracks comprehensive body metrics)
class WeighIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_logged = db.Column(db.Date, nullable=False, default=date.today)
    
    # The 10 Metrics
    weight_lbs = db.Column(db.Float, nullable=False)
    fat_pct = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    bmr_kcal = db.Column(db.Float, nullable=False)
    visceral_fat = db.Column(db.Float, nullable=False) 
    muscle_lbs = db.Column(db.Float, nullable=False)
    bone_mass_lbs = db.Column(db.Float, nullable=False)
    protein_pct = db.Column(db.Float, nullable=False)
    water_pct = db.Column(db.Float, nullable=False)
    skeletal_muscle_lbs = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"WeighIn('{self.date_logged}', {self.weight_lbs} lbs)"

# --- HELPER FUNCTION: DATE PARSING ---
def parse_date_input(date_str):
    """Converts a YYYY-MM-DD string from an HTML date input to a Python date object."""
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return date.today()

# --- CONTEXT PROCESSOR ---
# This function makes the 'datetime' object available to ALL Jinja2 templates
@app.context_processor
def inject_global_vars():
    # We return a dictionary where the key is the name used in the template (e.g., 'datetime')
    # and the value is the Python object (the datetime module itself)
    return {'datetime': datetime}

# --- ROUTES (The Controller Logic) ---

# Food Item Dictionary Management (NEW)
@app.route('/manage_food', methods=['GET', 'POST'])
def manage_food():
    if request.method == 'POST':
        # Get data for the new dictionary entry
        name = request.form.get('name').strip()
        
        # Validation and parsing
        if not name:
            # We would use flash messaging for errors in a real app, but for simplicity, we return the error template
            return render_template('error.html', message="Food name is required."), 400
        
        try:
            calories = int(request.form.get('calories') or 0)
            protein = float(request.form.get('protein') or 0)
            carbs = float(request.form.get('carbs') or 0)
            fat = float(request.form.get('fat') or 0)
        except ValueError:
            return render_template('error.html', message="Invalid numeric input for macros."), 400

        # Create and save the new FoodItem dictionary entry
        new_item = FoodItem(
            name=name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat
        )
        
        try:
            db.session.add(new_item)
            db.session.commit()
        except:
            # Handle unique constraint violation (if food name already exists)
            db.session.rollback()
            return render_template('error.html', message="Food item already exists in the dictionary!"), 400

        return redirect(url_for('manage_food'))
    
    else:
        # GET request: Display all existing dictionary items and the form to add a new one
        dictionary_items = FoodItem.query.order_by(FoodItem.name).all()
        return render_template('manage_food.html', dictionary_items=dictionary_items)

# The Main Dashboard and Food Logging Route (UPDATED)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Get Food Item ID and Quantity/Serving Size
        food_item_id = request.form.get('food_item_id')
        try:
            # Get the serving multiplier
            serving_multiplier = float(request.form.get('serving_multiplier') or 1.0)
            notes = request.form.get('notes')
            log_date = parse_date_input(request.form.get('date_eaten')) 
        except ValueError:
            return render_template('error.html', message="Invalid numeric input for serving size."), 400

        # 2. Look up the Food Item from the dictionary
        source_item = FoodItem.query.get(food_item_id)
        if not source_item:
            return render_template('error.html', message="Selected Food Item not found in dictionary. Please add it first."), 400

        # 3. Calculate final macros based on multiplier
        final_calories = int(source_item.calories * serving_multiplier)
        final_protein = source_item.protein * serving_multiplier
        final_carbs = source_item.carbs * serving_multiplier
        final_fat = source_item.fat * serving_multiplier
        
        # 4. Create the new FoodEntry log
        new_entry = FoodEntry(
            food_item_id=food_item_id,
            food_name=source_item.name,
            serving_multiplier=serving_multiplier,
            calories=final_calories,
            protein=final_protein,
            carbs=final_carbs,
            fat=final_fat,
            notes=notes,
            date_eaten=log_date
        )

        # 5. Save to the database
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('index'))

    else:
        # GET request: Fetch all dictionary items to populate the dropdown menu
        food_dictionary = FoodItem.query.order_by(FoodItem.name).all()
        # Fetch recent logs for the display table (Newest first)
        recent_food_entries = FoodEntry.query.order_by(FoodEntry.date_eaten.desc(), FoodEntry.id.desc()).limit(10).all()
        
        return render_template('index.html', 
                               food_entries=recent_food_entries,
                               food_dictionary=food_dictionary, 
                               today=date.today().strftime('%Y-%m-%d')) # Pass today's date for HTML input default

# Activity Logging Route (IMPLEMENTED)
@app.route('/log/activity', methods=['GET', 'POST'])
def log_activity():
    if request.method == 'POST':
        # 1. Get data from the form
        activity_type = request.form.get('activity_type')
        
        try:
            # Safely cast numeric inputs, defaulting to 0 if empty
            duration = float(request.form.get('duration_minutes') or 0)
            calories = int(request.form.get('calories_burned') or 0)
            # Distance is optional
            distance = float(request.form.get('distance_miles') or 0) 
            notes = request.form.get('notes')
            log_date = parse_date_input(request.form.get('date_logged')) 
        except ValueError:
            return render_template('error.html', message="Invalid numeric input for duration, calories, or distance."), 400

        # 2. Essential Validation: Must have type, duration, and calories burned
        if not activity_type or duration <= 0 or calories <= 0:
            return render_template('error.html', message="Activity type, duration, and calories burned are required."), 400

        # 3. Create the new database entry
        new_entry = ActivityEntry(
            activity_type=activity_type,
            duration_minutes=duration,
            calories_burned=calories,
            distance_miles=distance,
            notes=notes,
            date_logged=log_date
        )

        # 4. Save to the database
        db.session.add(new_entry)
        db.session.commit()

        # Redirect to show the updated list
        return redirect(url_for('log_activity'))

    else:
        # GET request: Display the activity logging form and recent entries
        # Fetch recent logs for display (Newest first)
        recent_activities = ActivityEntry.query.order_by(ActivityEntry.date_logged.desc(), ActivityEntry.id.desc()).limit(10).all()
        # Pass today's date and the activities to the template
        return render_template('log_activity.html', 
                               activities=recent_activities, 
                               today=date.today().strftime('%Y-%m-%d'))

# Metrics Logging Route (IMPLEMENTED)
@app.route('/log/metrics', methods=['GET', 'POST'])
def log_metrics():
    if request.method == 'POST':
        # 1. Get the date and all 10 metric fields
        try:
            log_date = parse_date_input(request.form.get('date_logged')) 
            
            # Use float casting with error handling for all 10 BeWell metrics
            weight = float(request.form.get('weight_lbs') or 0)
            fat = float(request.form.get('fat_pct') or 0)
            bmi = float(request.form.get('bmi') or 0)
            bmr = float(request.form.get('bmr_kcal') or 0)
            visceral_fat = float(request.form.get('visceral_fat') or 0)
            muscle = float(request.form.get('muscle_lbs') or 0)
            bone_mass = float(request.form.get('bone_mass_lbs') or 0)
            protein = float(request.form.get('protein_pct') or 0)
            water = float(request.form.get('water_pct') or 0)
            skeletal_muscle = float(request.form.get('skeletal_muscle_lbs') or 0)
        
        except ValueError:
            return render_template('error.html', message="All metrics must be valid numbers."), 400

        # 2. Basic Validation: Ensure weight is logged
        if weight <= 0:
            return render_template('error.html', message="Weight must be entered to log metrics."), 400

        # 3. Create a single WeighIn object (one row for 10 BeWell metrics)
        new_entry = WeighIn(
            date_logged=log_date,
            weight_lbs=weight,
            fat_pct=fat,
            bmi=bmi,
            bmr_kcal=bmr,
            visceral_fat=visceral_fat,
            muscle_lbs=muscle,
            bone_mass_lbs=bone_mass,
            protein_pct=protein,
            water_pct=water,
            skeletal_muscle_lbs=skeletal_muscle
        )

        # 4. Save to the database
        db.session.add(new_entry)
        db.session.commit()

        # Redirect to show the updated list
        return redirect(url_for('log_metrics'))

    else:
        # GET request: Display the metrics form and recent weigh-ins
        recent_weighins = WeighIn.query.order_by(WeighIn.date_logged.desc(), WeighIn.id.desc()).limit(10).all()
        return render_template('log_metrics.html', 
                               weighins=recent_weighins,
                               today=date.today().strftime('%Y-%m-%d'))

# Summary Page Route (IMPLEMENTED)
@app.route('/summary')
def summary():
    # 1. Fetch all necessary data from the database
    all_food = FoodEntry.query.all()
    all_activity = ActivityEntry.query.all()
    all_weighins = WeighIn.query.all() # Fetch all weigh-ins for BMR lookup
    
    # 2. Calculate daily macros and net calories (NOW includes BMR)
    daily_totals = calculate_daily_summary(all_food, all_activity, all_weighins)
    
    # 3. Analyze metric trends (Requires at least two entries to calculate change)
    metric_trends = analyze_metric_trends(all_weighins)

    # 4. Get the very last weigh-in for the dashboard view
    latest_weighin = all_weighins[-1] if all_weighins else None

    return render_template('summary.html',
                           daily_totals=daily_totals,
                           metric_trends=metric_trends,
                           latest_weighin=latest_weighin)

# History/Time-Based Filtering Route 
@app.route('/history', methods=['GET'])
def history():
    # 1. Get the date filter parameters from the URL
    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')
    
    # 2. Convert date strings to date objects for database queries
    start_date = parse_date_input(start_date_str) if start_date_str else None
    end_date = parse_date_input(end_date_str) if end_date_str else None
    
    # 3. Build the database query dynamically based on filters
    query = FoodEntry.query.order_by(FoodEntry.date_eaten.desc())
    
    if start_date:
        query = query.filter(FoodEntry.date_eaten >= start_date)
    if end_date:
        query = query.filter(FoodEntry.date_eaten <= end_date)
        
    # 4. Execute the query
    filtered_entries = query.all()
    
    # Pass the filtered results and the filters back to the template
    return render_template('history.html', 
                           filtered_entries=filtered_entries,
                           start_date=start_date_str, 
                           end_date=end_date_str)

# --- ADDITIONAL ERROR HANDLER (Good CS50x Practice) ---
@app.errorhandler(404)
def page_not_found(e):
    # This renders an error page if a user tries to access a non-existent URL
    return render_template('error.html', message=f"404 Error: The requested page was not found."), 404

# --- APPLICATION START ---
if __name__ == '__main__':
    with app.app_context():
        # Create all tables (FoodItem, FoodEntry, ActivityEntry, WeighIn)
        db.create_all() 
        
        # BONUS: Pre-populate the dictionary with an example item if it's empty
        if FoodItem.query.count() == 0:
            print("Pre-populating Food Dictionary...")
            example_item = FoodItem(name="Default Protein Shake", calories=160, protein=30.0, carbs=5.0, fat=2.0)
            db.session.add(example_item)
            db.session.commit()
            print("Pre-population complete.")
            
    app.run(debug=True)
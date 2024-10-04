from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the CSV with APOD data
csv_filename = 'apod_last_3_months_with_predefined_tags.csv'
df = pd.read_csv(csv_filename)

# Helper function to get today's APOD
# Helper function to get today's APOD
def get_today_apod():
    today_date = datetime.today().strftime('%Y-%m-%d')
    today_apod_df = df[df['date'] == today_date]
    
    # Check if the filtered DataFrame is empty
    if today_apod_df.empty:
        return None
    else:
        return today_apod_df.iloc[0]  # Return the first (and only) row as a Series


# Route for the home page
# Route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    today_apod = get_today_apod()
    
    # List of categories, months, and years
    categories = [
        'Nebulae and Star Formation',
        'Star Clusters',
        'Galaxies and Galaxy Interactions',
        'Exoplanets and Planetary Systems',
        'Black Holes and AGN',
        'Solar System Objects and Space Missions',
        'Astronomical Phenomena and Cosmic Events',
        'Earth-based Astronomical and Atmospheric Phenomena',
        'Astronomical Surveys and Observations',
        'Cosmic History and Evolution',
        'OTHERS'
    ]
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = sorted(df['date'].str[:4].unique(), reverse=True)  # Dynamically get available years from the CSV
    
    selected_category = request.form.get('category', 'Select Category')
    selected_month = request.form.get('month', '')
    selected_year = request.form.get('year', '')
    
    filtered_apods = df.copy()  # Start with the full DataFrame
    
    # Apply category filter if selected
    if selected_category != 'Select Category':
        filtered_apods = filtered_apods[filtered_apods['tags'].str.contains(selected_category, case=False, na=False)]
    
    # Apply month filter if selected
    if selected_month:
        month_number = months.index(selected_month) + 1  # Convert month name to number (1-12)
        filtered_apods = filtered_apods[pd.to_datetime(filtered_apods['date']).dt.month == month_number]
    
    # Apply year filter if selected
    if selected_year:
        filtered_apods = filtered_apods[pd.to_datetime(filtered_apods['date']).dt.year == int(selected_year)]
    
    filtered_apods = filtered_apods.to_dict('records')

    return render_template(
        "index.html",
        today_apod=today_apod,
        categories=categories,
        selected_category=selected_category,
        months=months,
        years=years,
        selected_month=selected_month,
        selected_year=selected_year,
        filtered_apods=filtered_apods
    )



# Route to handle individual APOD details
@app.route("/apod/<apod_date>")
def apod_details(apod_date):
    apod = df[df['date'] == apod_date].iloc[0] if not df[df['date'] == apod_date].empty else None
    if apod is None:
        return "APOD not found", 404
    return render_template("apod_details.html", apod=apod)

if __name__ == "__main__":
    app.run(debug=True)


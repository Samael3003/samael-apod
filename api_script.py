import csv
import requests
from datetime import datetime, timedelta

# Function to categorize APOD descriptions into predefined tags
def categorize_apod(description):
    # Define tags and corresponding keywords
    tags_keywords = {
        'Nebulae and Star Formation': ['nebula', 'star formation', 'stellar nursery', 'protostar'],
        'Star Clusters': ['star cluster', 'open cluster', 'globular cluster'],
        'Galaxies and Galaxy Interactions': ['galaxy', 'galaxies', 'merging galaxies', 'andromeda', 'milky way'],
        'Exoplanets and Planetary Systems': ['exoplanet', 'planetary system', 'kepler', 'habitable zone', 'jupiter'],
        'Black Holes and AGN': ['black hole', 'agn', 'active galactic nucleus', 'singularity'],
        'Solar System Objects and Space Missions': ['mars', 'jupiter', 'venus', 'comet', 'asteroid', 'space mission', 'satellite'],
        'Astronomical Phenomena and Cosmic Events': ['eclipse', 'supernova', 'gamma-ray burst', 'solar flare', 'meteor shower'],
        'Earth-based Astronomical and Atmospheric Phenomena': ['aurora', 'atmosphere', 'earth', 'lightning', 'weather'],
        'Astronomical Surveys and Observations': ['survey', 'telescope', 'observatory', 'spitzer', 'hubble'],
        'Cosmic History and Evolution': ['big bang', 'early universe', 'cosmology', 'dark matter', 'dark energy'],
        'OTHERS': []  # Fallback category for descriptions that don't match any keywords
    }

    # Convert description to lowercase for easier matching
    description = description.lower()

    # List to hold the assigned tags
    assigned_tags = []

    # Loop through the tags and check for matching keywords in the description
    for tag, keywords in tags_keywords.items():
        if any(keyword in description for keyword in keywords):
            assigned_tags.append(tag)
            if len(assigned_tags) == 3:  # Limit to 3 tags per article
                break

    # If no tags were found, assign 'OTHERS'
    if not assigned_tags:
        assigned_tags.append('OTHERS')

    return ', '.join(assigned_tags)

# Get APOD data for the last 3 months
BASE_URL = 'https://api.nasa.gov/planetary/apod'
NASA_API_KEY = '1ziSJAz9HF9xnGon765U1ymA4cUQ1vMIaROe35K0'

# Date range (last 3 months)
end_date = datetime.today()
start_date = end_date - timedelta(days=730)

# Prepare the CSV file
csv_filename = 'apod_last_3_months_with_predefined_tags.csv'

# Define CSV columns
csv_columns = ['date', 'title', 'url', 'hdurl', 'explanation', 'tags']

# Open the CSV file to write
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()

    # Loop over the dates
    current_date = start_date
    while current_date <= end_date:
        # Format the date as YYYY-MM-DD
        date_str = current_date.strftime('%Y-%m-%d')

        # Make the API call to APOD
        params = {
            'api_key': NASA_API_KEY,
            'date': date_str
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract APOD details
            date = data.get('date', '')
            title = data.get('title', '')
            url = data.get('url', '')
            hdurl = data.get('hdurl', '')
            explanation = data.get('explanation', '')

            # Get tags for the APOD description using offline categorization
            tags = categorize_apod(explanation)

            # Prepare the row for CSV
            row = {
                'date': date,
                'title': title,
                'url': url,
                'hdurl': hdurl,
                'explanation': explanation,
                'tags': tags
            }

            # Write the row to the CSV file
            writer.writerow(row)

        # Move to the next day
        current_date += timedelta(days=1)

print(f"APOD data with predefined tags saved to {csv_filename}")


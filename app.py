from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# === Helper function to fetch crime data ===

def fetch_crime_data():
    URL = "https://data.princegeorgescountymd.gov/resource/xjru-idbe.json"
    today = datetime.today().date()
    days_since_friday = (today.weekday() - 4) % 7
    last_friday = today - timedelta(days=days_since_friday)
    previous_friday = last_friday - timedelta(days=14)

    start_date_str = previous_friday.isoformat()
    end_date_str = last_friday.isoformat()

    url_with_dates = f"{URL}?$where=date >= '{start_date_str}' AND date <= '{end_date_str}'&$order=date DESC"
    response = requests.get(url_with_dates)

    if response.status_code == 200:
        return response.json()
    else:
        return []

# === Routes ===

@app.route('/')
def home():
    data = fetch_crime_data()
    violent_crimes = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'SEX OFFENSE', 'SHOOTING']

    crime_type_counter = {}

    for crime in data:
        crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
        if any(violent in crime_type for violent in violent_crimes):
            crime_type_counter[crime_type] = crime_type_counter.get(crime_type, 0) + 1

    return render_template('home.html', crime_counts=crime_type_counter)

@app.route('/map')
def map_view():
    data = fetch_crime_data()
    violent_crimes = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'SEX OFFENSE', 'SHOOTING']

    crime_locations = []

    for crime in data:
        crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
        if any(violent in crime_type for violent in violent_crimes):
            lat = crime.get('latitude')
            lng = crime.get('longitude')
            if lat and lng:
                crime_locations.append({
                    'type': crime_type,
                    'lat': float(lat),
                    'lng': float(lng),
                    'address': crime.get('street_address', 'Unknown Address')
                })

    return render_template('map.html', crimes=crime_locations)

# === Run the app ===

if __name__ == '__main__':
    app.run(debug=True)

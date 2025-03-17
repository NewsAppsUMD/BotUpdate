import requests
import json
import pandas as pd
from datetime import datetime

# Constants
URL = 'https://data.princegeorgescountymd.gov/resource/xjru-idbe.json'
VIOLENT_CRIMES = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'SEX OFFENSE']

# Step 1: Fetch the data
def fetch_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("Data fetched and saved successfully.")
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Step 2: Process the data
def process_data():
    # Load data from file
    df = pd.read_json('data.json')

    # Filter necessary fields
    df = df[['incident_case_id', 'date', 'clearance_code_inc_type', 'street_address', 'latitude', 'longitude']]

    # Classify crimes
    df['crime_type'] = df['clearance_code_inc_type'].apply(
        lambda x: 'Violent' if x in VIOLENT_CRIMES else 'Non-Violent'
    )

    # Format date
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Save processed data to a new file
    df.to_json('processed_data.json', orient='records', indent=2)
    print("Data processed successfully.")

# Step 3: Send notification (logging the data instead of Telegram)
def send_notification():
    with open('processed_data.json', 'r') as f:
        data = json.load(f)

    latest_crime = data[0]  # Get latest crime record
    message = (f"🚨 {latest_crime['crime_type']} - {latest_crime['clearance_code_inc_type']}\n"
               f"📍 {latest_crime['street_address']}\n"
               f"🕒 {latest_crime['date']}")

    # Log message to console
    print("Notification sent:")
    print(message)

# Main function to execute the process
if __name__ == "__main__":
    fetch_data()
    process_data()
    send_notification()

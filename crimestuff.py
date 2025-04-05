import requests
from datetime import datetime, timedelta

# Constants
URL = "https://data.princegeorgescountymd.gov/resource/xjru-idbe.json"

# Today
today = datetime.today().date()

# Calculate last Friday
days_since_friday = (today.weekday() - 4) % 7
last_friday = today - timedelta(days=days_since_friday)

# Calculate previous Friday (1 week before last Friday = 2 weeks before today)
previous_friday = last_friday - timedelta(days=14)

# Optional: If the API lags more, go back 2 full weeks instead of 1
# previous_friday = last_friday - timedelta(days=14)

# Format date strings
start_date_str = previous_friday.isoformat()
end_date_str = last_friday.isoformat()

# Fetch the data from the specified date range
url_with_dates = f"{URL}?$where=date >= '{start_date_str}' AND date <= '{end_date_str}'&$order=date DESC"
response = requests.get(url_with_dates)

if response.status_code == 200:
    data = response.json()
    
    violent_crimes = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'SEX OFFENSE', 'SHOOTING']
    
    violent_crime_count = 0
    crime_summaries = []
    
    if data:
        for crime in data:
            crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
            
            if any(violent in crime_type for violent in violent_crimes):
                violent_crime_count += 1
                crime_date = crime.get('date', 'Unknown Date')
                street_address = crime.get('street_address', 'Unknown Address')
                crime_summaries.append(f"Date: {crime_date}, Type: {crime_type}, Address: {street_address}")
        
        if violent_crime_count > 0:
            print(f"\nSummary of Violent Crimes from {start_date_str} to {end_date_str}:")
            for summary in crime_summaries:
                print(summary)
            
            print(f"\nTotal Violent Crimes: {violent_crime_count}")
            print(f"\nSummary: The past week ({start_date_str} to {end_date_str}) saw a total of {violent_crime_count} violent incidents. Notable locations included {', '.join([summary.split('Address: ')[-1] for summary in crime_summaries])}.")
        else:
            print(f"\nNo violent crimes reported between {start_date_str} and {end_date_str}.")
    else:
        print(f"\nNo data available for the specified range.")
else:
    print(f"Error fetching data: {response.status_code}")

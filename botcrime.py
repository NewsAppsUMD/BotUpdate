import requests
from datetime import datetime

# Constants
URL = "https://data.princegeorgescountymd.gov/resource/xjru-idbe.json"

# Define the date range from March 21st to March 28th
start_date_str = '2025-03-21'
end_date_str = '2025-03-28'

# Fetch the data from the specified date range
url_with_dates = f"{URL}?$where=date >= '{start_date_str}' AND date <= '{end_date_str}'&$order=date DESC"
response = requests.get(url_with_dates)

if response.status_code == 200:
    data = response.json()
    
    # Define violent crime types
    violent_crimes = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'SEX OFFENSE', 'SHOOTING']
    
    # Initialize counters and summary lists
    violent_crime_count = 0
    crime_summaries = []
    
    # Process the data for violent crimes
    if data:
        for crime in data:
            crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
            
            # Check if the crime is violent
            if any(violent in crime_type for violent in violent_crimes):
                violent_crime_count += 1
                crime_date = crime.get('date', 'Unknown Date')
                street_address = crime.get('street_address', 'Unknown Address')
                crime_summaries.append(f"Date: {crime_date}, Type: {crime_type}, Address: {street_address}")
        
        # If there are violent crimes, summarize
        if violent_crime_count > 0:
            print(f"\nSummary of Violent Crimes from {start_date_str} to {end_date_str}:")
            for summary in crime_summaries:
                print(summary)
            
            # Compose a summary in a few sentences
            print(f"\nTotal Violent Crimes: {violent_crime_count}")
            print(f"\nSummary: The past week ({start_date_str} to {end_date_str}) saw a total of {violent_crime_count} violent incidents. These incidents included assault, shooting, and other violent crimes. Notable locations included {', '.join([summary.split('Address: ')[-1] for summary in crime_summaries])}.")
        else:
            print(f"\nNo violent crimes reported between {start_date_str} and {end_date_str}.")
    else:
        print(f"\nNo data available for the specified range.")
else:
    print(f"Error fetching data: {response.status_code}")

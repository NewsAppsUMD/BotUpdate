import requests
from datetime import datetime, timedelta
from collections import Counter  # 🔑 For counting crime types

# Constants
URL = "https://data.princegeorgescountymd.gov/resource/xjru-idbe.json"

# Today
today = datetime.today().date()

# Calculate last Friday
days_since_friday = (today.weekday() - 4) % 7
last_friday = today - timedelta(days=days_since_friday)

# Calculate previous Friday (2 weeks before last Friday)
previous_friday = last_friday - timedelta(days=14)

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
    crime_type_counter = Counter()  # 🧮 Count each type of violent crime
    crime_summaries = []
    
    if data:
        for crime in data:
            crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
            
            if any(violent in crime_type for violent in violent_crimes):
                violent_crime_count += 1
                crime_type_counter[crime_type] += 1  # ⬅️ Count this crime type
                crime_date = crime.get('date', 'Unknown Date')
                street_address = crime.get('street_address', 'Unknown Address')
                
                formatted = (
                    f"\n--- Crime #{violent_crime_count} ---\n"
                    f"📅 Date: {crime_date}\n"
                    f"🔪 Type: {crime_type}\n"
                    f"📍 Address: {street_address}\n"
                )
                
                crime_summaries.append(formatted)
        
        if violent_crime_count > 0:
            print(f"\n🧾 Summary of Violent Crimes from {start_date_str} to {end_date_str}:\n")
            for summary in crime_summaries:
                print(summary)
            
            print(f"\n📊 Total Violent Crimes: {violent_crime_count}")
            
            # 🔠 Build summary line with breakdown
            crime_breakdown = ', '.join([
                f"{count} {ctype.lower()}{'s' if count > 1 else ''}" 
                for ctype, count in crime_type_counter.items()
            ])
            
            print(f"\n🗒️ Summary: Between {start_date_str} and {end_date_str}, there were {violent_crime_count} violent crimes reported. Breakdown: {crime_breakdown}.")
        else:
            print(f"\n✅ No violent crimes reported between {start_date_str} and {end_date_str}.")
    else:
        print(f"\n⚠️ No data available for the specified range.")
else:
    print(f"❌ Error fetching data: {response.status_code}")

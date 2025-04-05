import requests
from datetime import datetime, timedelta
from collections import Counter  # 🔑 For counting crime types

# === SLACK SETUP ===
def send_to_slack(message, webhook_url):
    payload = {"text": message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response.status_code == 200

# 🔗 Your Slack Webhook URL here
WEBHOOK_URL = "https://hooks.slack.com/services/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"

# === CRIME DATA SETUP ===
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
    crime_type_counter = Counter()
    crime_summaries = []
    
    if data:
        for crime in data:
            crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
            
            if any(violent in crime_type for violent in violent_crimes):
                violent_crime_count += 1
                crime_type_counter[crime_type] += 1
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
            # Print locally
            print(f"\n🧾 Summary of Violent Crimes from {start_date_str} to {end_date_str}:\n")
            for summary in crime_summaries:
                print(summary)
            print(f"\n📊 Total Violent Crimes: {violent_crime_count}")
            
            # Create breakdown
            crime_breakdown = ', '.join([
                f"{count} {ctype.lower()}{'s' if count > 1 else ''}"
                for ctype, count in crime_type_counter.items()
            ])
            
            # Slack message
            slack_message = (
    f"📊 *PG County Weekly Crime Summary*\n"
    f"📅 *Period:* {start_date_str} to {end_date_str}\n"
    f"🔢 *Total Violent Crimes:* {violent_crime_count}\n"
    f"🔍 *Breakdown:* {crime_breakdown}\n\n"
    f"🌐 *Resources:*\n"
    f"• [Crime Map & Stats](https://www.princegeorgescountymd.gov/345/Public-Safety)\n"
    f"• [Submit a Tip](https://www.pgcrimesolvers.com/)\n"
    f"• [Join/Start a Neighborhood Watch](https://www.princegeorgescountymd.gov/849/Neighborhood-Watch)\n\n"
    f"📢 *Action You Can Take:*\n"
    f"If you see something suspicious, say something. Stay alert and connected.\n"
)

        else:
            slack_message = f"✅ No violent crimes reported in PG County from {start_date_str} to {end_date_str}."
        
        # Send to Slack
        if send_to_slack(slack_message, WEBHOOK_URL):
            print("✅ Slack notification sent.")
        else:
            print("❌ Failed to send Slack notification.")

    else:
        print(f"\n⚠️ No data available for the specified range.")
else:
    print(f"❌ Error fetching data: {response.status_code}")
import requests
from datetime import datetime, timedelta
from collections import Counter
from dotenv import load_dotenv
import os# 🔑 For counting crime types



load_dotenv()

# Retrieve the variables
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL")

print(f"SLACK_BOT_TOKEN: {slack_bot_token}")
print(f"SLACK_CHANNEL: {slack_channel}")




#load_dotenv()
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#general")  # Set your target channel name or ID
client = WebClient(token=SLACK_BOT_TOKEN)

def send_to_slack(message):
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        return response["ok"]
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")
        return False



# === CRIME DATA SETUP ===
# Constants
URL = "https://data.princegeorgescountymd.gov/resource/xjru-idbe.json"

# Today
today = datetime.today().date()

# Calculating last Friday
days_since_friday = (today.weekday() - 4) % 7
last_friday = today - timedelta(days=days_since_friday)

# Calculating previous Friday (2 weeks before last Friday)
previous_friday = last_friday - timedelta(days=14)

# Formatring date strings
start_date_str = previous_friday.isoformat()
end_date_str = last_friday.isoformat()

# Fetching the data from the specified date range
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
            
            # Creating breakdown
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
    f"• [Daily Crime Report](https://dailycrime.princegeorgescountymd.gov/)\n"
    f"• [Submit a Tip](https://www.pgcrimesolvers.com/)\n"
    f"• [PG County Police Important Numbers](https://www.princegeorgescountymd.gov/departments-offices/police/important-phone-numbers/)\n\n"
    f"📢 *Action You Can Take:*\n"
    f"If you see something suspicious, say something. Stay alert and connected.\n"
)

        else:
            slack_message = f"✅ No violent crimes reported in PG County from {start_date_str} to {end_date_str}."
        
        # Sending to Slack
        if send_to_slack(slack_message):
            print("✅ Slack notification sent.")
        else:
            print("❌ Failed to send Slack notification.")

    else:
        print(f"\n⚠️ No data available for the specified range.")
else:
    print(f"❌ Error fetching data: {response.status_code}") 
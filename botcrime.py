from database_pg import insert_crime_if_new
import requests
from datetime import datetime, timedelta
from collections import Counter
from dotenv import load_dotenv
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# === Load Slack credentials ===
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
client = WebClient(token=SLACK_BOT_TOKEN)

def send_to_slack(message):
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        return response["ok"]
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")
        return False

# === Crime Data Setup ===
API_URL = "https://data.princegeorgescountymd.gov/resource/xjru-idbe.json"
LIMIT = 1000
OFFSET = 0

# Time Range: Last two weeks before last Friday
today = datetime.today().date()
start_date = today - timedelta(days=21)

# Format as MM/DD/YYYY because that's how the API stores it
start_date_str = start_date.strftime("%m/%d/%Y")
end_date_str = today.strftime("%m/%d/%Y")

# Pull all records via pagination
all_crime_data = []
while True:
    query_url = (
        f"{API_URL}?$limit={LIMIT}&$offset={OFFSET}"
        f"&$where=date >= '{start_date_str}' AND date <= '{end_date_str}'"
    )
    response = requests.get(query_url)
    if response.status_code != 200:
        print(f"❌ Error fetching data: {response.status_code}")
        break

    batch = response.json()
    if not batch:
        break  # Exit loop when there's no more data

    all_crime_data.extend(batch)
    OFFSET += LIMIT  # Get next page

print(f"✅ Retrieved {len(all_crime_data)} records.")

# === Filter for Violent Crimes ===
violent_crimes = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'SEX OFFENSE', 'SHOOTING']
violent_crime_count = 0
crime_type_counter = Counter()
crime_summaries = []

for crime in all_crime_data:
    crime_type = crime.get('clearance_code_inc_type', 'Unknown').upper()
    if any(v in crime_type for v in violent_crimes):
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

        #
        insert_crime_if_new(crime)


# === Create Slack Message ===
if violent_crime_count > 0:
    crime_breakdown = ', '.join([
        f"{count} {ctype.lower()}{'s' if count > 1 else ''}"
        for ctype, count in crime_type_counter.items()
    ])
    preview = "\n".join(crime_summaries[:3])  # Show top 3

    slack_message = (
        f"📊 *PG County Weekly Crime Summary*\n"
        f"📅 *Period:* {start_date_str} to {end_date_str}\n"
        f"🔢 *Total Violent Crimes:* {violent_crime_count}\n"
        f"🔍 *Breakdown:* {crime_breakdown}\n\n"
        f"🧾 *Sample Incidents:*\n{preview}\n\n"
        f"🌐 *Resources:*\n"
        f"• [Daily Crime Report](https://dailycrime.princegeorgescountymd.gov/)\n"
        f"• [Submit a Tip](https://www.pgcrimesolvers.com/)\n"
        f"• [Police Contacts](https://www.princegeorgescountymd.gov/departments-offices/police/important-phone-numbers/)\n\n"
        f"📢 *Action You Can Take:*\n"
        f"If you see something suspicious, say something."
    )
else:
    slack_message = f"✅ No violent crimes reported in PG County from {start_date_str} to {end_date_str}."

# === Send to Slack ===
if send_to_slack(slack_message):
    print("✅ Slack notification sent.")
else:
    print("❌ Failed to send Slack notification.")

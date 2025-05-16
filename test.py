from slack_sdk import WebClient
import os
from dotenv import load_dotenv

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
channel = os.getenv("SLACK_CHANNEL")

response = client.chat_postMessage(channel=channel, text="Hello from BlueEyesWhiteDragon!")
print(response)

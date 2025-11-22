import os, requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("WILIO_AUTH_TOKEN")
FROM_WHATSAPP = "whatsapp:+14155238886"         # Twilio sandbox number
TO_WHATSAPP = "whatsapp:+919901659905"          # your number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp(msg):
    client.messages.create(
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP,
        body=msg
    )

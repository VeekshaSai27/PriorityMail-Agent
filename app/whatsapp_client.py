# app/whatsapp_client.py
import os
from twilio.rest import Client
from dotenv import load_dotenv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


TW_SID = os.getenv("TWILIO_SID")
TW_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM = os.getenv("TWILIO_WHATSAPP_FROM")  
TO = os.getenv("TWILIO_WHATSAPP_TO")      

client = Client(TW_SID, TW_TOKEN)

def send_whatsapp_message(message_text):
    if not (TW_SID and TW_TOKEN and FROM and TO):
        print("⚠️ Missing Twilio environment variables")
        return
    
    try:
        msg = client.messages.create(
            from_=FROM,
            body=message_text,
            to=TO
        )
        print(f"✔️ WhatsApp sent: {msg.sid}")
        return msg.sid
    except Exception as e:
        print(f"❌ WhatsApp send error: {e}")
        return None

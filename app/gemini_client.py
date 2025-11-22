# app/gemini_client.py
import os, requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "models/gemini-2.5-flash"   # change to the model you have access to

BASE_URL = "https://generativelanguage.googleapis.com/v1"

def generate_text(prompt, max_retries=3):
    url = f"{BASE_URL}/{MODEL}:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        # you can tune safety/temperature etc here if supported by API
    }
    for attempt in range(max_retries):
        r = requests.post(url, headers=headers, params=params, json=data)
        if r.status_code == 200:
            try:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception:
                return None
        else:
            # exponential backoff on server errors/429/503
            if r.status_code in (429, 503):
                import time
                time.sleep(2 ** attempt)
                continue
            else:
                # for debugging, you may want to log r.text
                return None
    return None

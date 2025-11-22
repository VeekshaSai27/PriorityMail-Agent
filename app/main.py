# app/main.py
import warnings
warnings.filterwarnings("ignore")
from app.gmail_client import get_gmail_service
from app.fetcher import fetch_unread_emails
from app.summarizer import summarize_email
from app.classifier import classify_email_normalized
from app.storage import save_summary
from app.whatsapp_client import send_whatsapp_message
import time, json, os

# canonical categories set - used for clarity
URGENT_LABEL = "Urgent Emails"
IMPORTANT_LABEL = "Important Emails"

def print_email_block(sender, subject, brief_expl, category):
    """
    Print the exact format you requested.
    """
    print("sender:")
    print(sender)
    print()
    print("subject:")
    print(subject)
    print()
    print("content:")
    print(brief_expl)
    print()
    print("Detected type:", category)
    print("-" * 60)

def process_inbox():
    print("🚀 Starting AI Mail Agent (local run)...")
    service = get_gmail_service()
    print("🔍 Connected! Fetching unread emails...")
    emails = fetch_unread_emails(service)
    print(f"📥 Found {len(emails)} unread emails.\n")

    if not emails:
        print("No emails to process.")
        return

    for e in emails:
        sender = e.get("from", "Unknown sender")
        subject = e.get("subject", "(no subject)")
        body = e.get("body", "")

        # 1) summarize
        brief = summarize_email(body)

        # 2) classify
        category = classify_email_normalized(body)

        # 3) print block exactly as requested
        print_email_block(sender, subject, brief, category)

        # 4) save to local JSON
        data = {
            "from": sender,
            "subject": subject,
            "summary": brief,
            "category": category,
            "timestamp": int(time.time())
        }
        try:
            save_summary(data)
        except Exception as ex:
            print("⚠️ Warning: save_summary failed:", ex)

        # 5) WhatsApp allowed categories
        WHATSAPP_ALLOWED = {
            "Urgent Emails",
            "Important Emails",
            "Transactional Emails",
            "Informational Emails"
        }

        if category in WHATSAPP_ALLOWED:
            short_summary = (brief[:900] + "...") if len(brief) > 900 else brief
            
            whatsapp_text = (
                f"📨 *{category}*\n"
                f"👤 From: {sender}\n"
                f"📌 Subject: {subject}\n"
                f"📝 Summary: {short_summary}"
            )

            sid = send_whatsapp_message(whatsapp_text)
            if sid:
                print(f"✔️ WhatsApp sent: {sid}")
            else:
                print("❌ WhatsApp send failed.")

    print("\n✅ Done checking inbox!")

if __name__ == "__main__":
    process_inbox()



"""start app my saying python -m app.main"""
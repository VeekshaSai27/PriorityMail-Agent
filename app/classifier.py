# app/classifier.py
"""
Classifier wrapper that returns one of the following canonical labels:
1. Promotional Emails
2. Urgent Emails
3. Important Emails
4. Transactional Emails
5. Informational Emails
6. Personal Emails
7. System / Notification Emails
8. Work / Professional Emails
9. Spam / Junk Emails
10. Phishing Emails

Function to call from main.py: classify_email_normalized(body_text)
"""

import re

# If you already have a function that calls Gemini, keep using it and call it inside _raw_classify.
# For example: from gemini_client import classify_with_gemini
# But to keep this module independent we define a simple raw placeholder. Replace if needed.

def _raw_classify(body_text: str) -> str:
    """
    If you have an LLM-based classifier (e.g., gemini), call it here and return the raw label.
    Otherwise fall back to heuristics. Example raw labels could be 'important', 'promotional', etc.
    """

    b = (body_text or "").lower()

    # phishing heuristics
    if any(x in b for x in ["verify your account", "reset your password", "urgent action required", "confirm your account", "click here to verify"]):
        return "phishing"

    # transactional: receipts, order, invoice, payment
    if any(x in b for x in ["order number", "invoice", "receipt", "payment confirmation", "transaction id", "booking confirmation"]):
        return "transactional"

    # system/notification
    if any(x in b for x in ["system alert", "notification", "service update", "status update", "deployment", "downtime", "outage"]):
        return "system"

    # personal
    if any(x in b for x in ["hi ", "hey ", "regards,", "love,", "dear ", "best,", "sincerely", "from:"]):
        # this is fuzzy; keep last resort
        return "personal"

    # promotional
    if any(x in b for x in ["subscribe", "sale", "discount", "offer", "coupon", "free trial", "limited time", "deal", "unsubscribe"]):
        return "promotional"

    # spam heuristics
    if any(x in b for x in ["win money", "congratulations you have been selected", "act now", "click here to claim"]):
        return "spam"

    # default informational
    return "informational"


# mapping from raw label/heuristics to canonical categories
_mapping = {
    # keys map to canonical label strings below
    "promotional": "Promotional Emails",
    "promo": "Promotional Emails",
    "ad": "Promotional Emails",

    "urgent": "Urgent Emails",
    "high": "Urgent Emails",
    "action required": "Urgent Emails",

    "important": "Important Emails",
    "info": "Informational Emails",
    "informational": "Informational Emails",

    "transactional": "Transactional Emails",
    "receipt": "Transactional Emails",
    "order": "Transactional Emails",

    "personal": "Personal Emails",

    "system": "System / Notification Emails",
    "notification": "System / Notification Emails",

    "work": "Work / Professional Emails",
    "professional": "Work / Professional Emails",

    "spam": "Spam / Junk Emails",
    "phishing": "Phishing Emails",
}

# canonical labels set
CANONICAL = [
    "Promotional Emails",
    "Urgent Emails",
    "Important Emails",
    "Transactional Emails",
    "Informational Emails",
    "Personal Emails",
    "System / Notification Emails",
    "Work / Professional Emails",
    "Spam / Junk Emails",
    "Phishing Emails",
]

def classify_email_normalized(body_text: str) -> str:
    """
    Returns one of the 10 canonical labels.
    """
    if not body_text:
        return "Informational Emails"

    # try LLM/raw classifier first if you have one
    try:
        raw = _raw_classify(body_text)  # replace with your LLM call if available
    except Exception:
        raw = _raw_classify(body_text)

    raw = (raw or "").strip().lower()

    # map exact keys or words to canonical labels
    for key, canon in _mapping.items():
        if key in raw:
            return canon

    # fallback: look for keywords that indicate importance/urgency
    if any(w in body_text.lower() for w in ["urgent", "asap", "immediately", "action required", "deadline", "due by"]):
        return "Urgent Emails"

    if any(w in body_text.lower() for w in ["important", "please read", "required", "note that", "attention"]):
        return "Important Emails"

    # last resort: if body has many financial/transaction keywords
    if any(w in body_text.lower() for w in ["invoice", "receipt", "order", "booking", "payment"]):
        return "Transactional Emails"

    # default
    return "Informational Emails"

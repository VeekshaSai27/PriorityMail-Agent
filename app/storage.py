import json, os

def save_summary(data, filename="email_summaries.json"):
    if os.path.exists(filename):
        old = json.load(open(filename))
    else:
        old = []
    old.insert(0, data)
    json.dump(old, open(filename, "w"), indent=2)

import json
from typing import List, Dict

EMAILS_PATH = "emails.json"
SENT_PATH = "sent.json"

def load_emails() -> List[Dict]:
    with open(EMAILS_PATH, "r") as f:
        return json.load(f)

def append_to_sent(email: Dict):
    with open(SENT_PATH, "r+") as f:
        sent = json.load(f)
        sent.append(email)
        f.seek(0)
        json.dump(sent, f, indent=2)

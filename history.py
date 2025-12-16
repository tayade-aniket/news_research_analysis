import json
from datetime import datetime

FILE = "history.json"

def save_query(query, summary):
    entry = {
        "query": query,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_history():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

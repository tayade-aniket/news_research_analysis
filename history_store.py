import json
import os
from datetime import datetime

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "history.json")

def save_history(user: str, query: str):
    os.makedirs(DATA_DIR, exist_ok=True)

    history = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)

    history.append({
        "user": user,
        "query": query,
        "timestamp": str(datetime.now())
    })

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def load_history(user: str):
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        history = json.load(f)

    user_history = [
        h for h in history
        if h.get("user") == user and "query" in h
    ]

    user_history.reverse()
    return user_history

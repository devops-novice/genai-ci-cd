import json
from datetime import datetime
import os

LOG_FILE = "rag_eval_log.jsonl"
os.makedirs("logs", exist_ok=True)
LOG_PATH = os.path.join("logs", LOG_FILE)

def log_rag_eval(entry: dict):
    entry["timestamp"] = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

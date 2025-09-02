import json
from datetime import datetime
import os

# --- Minimal event logger for RAG ---
import json, logging, os

LOG_FILE = "rag_eval_log.jsonl"
os.makedirs("logs", exist_ok=True)
LOG_PATH = os.path.join("logs", LOG_FILE)

def log_rag_eval(entry: dict):
    entry["timestamp"] = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


# --- Minimal event logger for RAG ---

_logger = logging.getLogger("rag")
if not _logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    _logger.addHandler(_h)
    _logger.setLevel(getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO))

def log_event(event: str, data: dict) -> None:
    """Safe, lightweight structured log."""
    try:
        _logger.info("%s %s", event, json.dumps(data, ensure_ascii=False, sort_keys=True))
    except Exception as e:
        _logger.warning("log_event_failed %s %s", event, e)

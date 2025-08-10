# app/faithfulness.py
from typing import List, Dict

def check_faithfulness(answer: str, retrieved: List[Dict], relevant_ids: List[str], overlap_thresh: float = 0.6):
    # retrieved: [{"id": "doc#1", "text": "..."}]
    import re
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', answer) if s.strip()]
    def overlap(a, b):
        aw, bw = a.lower().split(), b.lower().split()
        inter = sum(min(aw.count(w), bw.count(w)) for w in set(aw))
        return inter / max(1, len(bw))
    rel_texts = [r["text"] for r in retrieved if r["id"] in relevant_ids]
    unsupported = []
    for s in sentences:
        ok = any(overlap(s, t) >= overlap_thresh for t in rel_texts)
        if not ok: unsupported.append(s)
    return {"supported": len(unsupported) == 0, "unsupported_spans": unsupported}

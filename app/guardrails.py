# app/guardrails.py
from typing import Tuple

SAFE_DOMAINS = {"reflections-week", "concepts.md", "AI_Leadership_Reading_Plan_Refined.md", "TASKS.md"}

def validate_input(query: str) -> Tuple[bool, str]:
    q = (query or "").strip()
    if not q:
        return False, "Empty query"
    if len(q) < 4:
        return False, "Query too short"
    return True, ""

def allow_domain(source: str) -> bool:
    # simple allowlist: pass if file basename starts with a safe prefix
    s = (source or "").lower()
    return any(s.startswith(dom) for dom in SAFE_DOMAINS)

def filter_retrieved(docs):
    """Drop docs whose source is off-domain."""
    return [d for d in docs if allow_domain(d.get("source"))]

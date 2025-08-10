# app/generator.py
from __future__ import annotations
from typing import List, Dict, Tuple
import re

def _sentences(text: str) -> List[str]:
    # simple, fast splitter; avoids heavy libs
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text or "") if s.strip()]
    return sents if sents else [text.strip()] if text else []

def _overlap_score(question: str, sentence: str) -> float:
    q = question.lower().split()
    s = sentence.lower().split()
    if not q or not s:
        return 0.0
    qset = set(q)
    inter = sum(1 for t in s if t in qset)
    return inter / len(s)  # fraction of sentence tokens that appear in question

def _best_sentence_for(question: str, passage: str) -> str:
    sents = _sentences(passage)
    if not sents:
        return ""
    return max(sents, key=lambda s: _overlap_score(question, s))

def generate_answer(
    question: str,
    retrieved: List[Dict],           # [{"id": "...", "text": "...", "source": "..."}]
    cfg: Dict | None = None
) -> Tuple[str, List[str]]:
    """
    Deterministic extractive generator:
    - Pick highest-overlap sentence from top doc
    - Optionally append another from the next doc if short
    Returns: (answer_text, used_ids)
    """
    cfg = cfg or {}
    min_words = int(cfg.get("min_words", 8))
    max_sentences = int(cfg.get("max_sentences", 2))

    if not retrieved:
        return "", []

    used_ids: List[str] = []
    pieces: List[str] = []

    # iterate through top-N docs until we gather enough words
    for doc in retrieved[:max_sentences]:
        best = _best_sentence_for(question, doc.get("text", ""))
        if best:
            pieces.append(best)
            used_ids.append(doc["id"])
        if len(" ".join(pieces).split()) >= min_words:
            break

    return " ".join(pieces).strip(), used_ids

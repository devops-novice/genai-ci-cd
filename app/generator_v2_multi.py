# app/generator_v2_multi.py
from __future__ import annotations
from typing import List, Dict, Tuple
import math, re

# ---- sentence utils ----
_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9(])')
def _tok(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9]+", text.lower())

def split_into_sentences(text: str) -> List[str]:
    text = re.sub(r'\s+', ' ', text.strip())
    out = []
    for para in re.split(r'\n{2,}', text):
        for s in _SENT_SPLIT.split(para.strip()):
            s = s.strip(" •*-–—")
            if len(s) >= 20:
                out.append(s)
    return out

# ---- scoring ----
def _idf(tokens: List[str]) -> Dict[str, float]:
    freq = {}
    for t in tokens:
        t = t.lower()
        freq[t] = freq.get(t, 0) + 1
    N = len(tokens) + 1
    return {t: math.log(N/(1+c)) for t, c in freq.items()}

def sentence_query_overlap_score(sentence: str, query: str) -> float:
    qs = set(_tok(query))
    st = _tok(sentence)
    if not st or not qs:
        return 0.0
    idf = _idf(st)
    return sum(idf.get(t, 0.0) for t in st if t in qs) / (1.0 + len(st))

def blended_sentence_score(sentence: str, query: str, parent_doc_score: float) -> float:
    r = 1.0 - math.exp(-max(0.0, parent_doc_score))  # squash retrieval score to [0,1]
    lex = sentence_query_overlap_score(sentence, query)
    return 0.65 * lex + 0.35 * r

# ---- selector ----
def _sim(a: str, b: str) -> float:
    # Jaccard on 3-grams
    def grams(x: str) -> set:
        toks = _tok(x)
        return set(zip(toks, toks[1:], toks[2:])) if len(toks) >= 3 else set(toks)
    A, B = grams(a), grams(b)
    if not A or not B:
        return 0.0
    return len(A & B) / (len(A | B) + 1e-9)

def select_supporting_sentences(
    retrieved: List[Dict],
    query: str,
    total_k: int = 6,
    max_per_doc: int = 3,
    dedupe_similarity: float = 0.85
):
    cand = []
    for d in retrieved:
        doc_id  = d.get("id") or d.get("doc_id") or "unknown"
        source  = d.get("source") or d.get("file") or "local"
        score   = float(d.get("score", 1.0))
        text    = d.get("text") or ""
        sents = split_into_sentences(text)
        scored = [(blended_sentence_score(s, query, score), s) for s in sents]
        scored.sort(key=lambda x: x[0], reverse=True)
        for sc, s in scored[:max_per_doc]:
            cand.append({"sentence": s, "doc_id": doc_id, "source": source, "score": sc})

    cand.sort(key=lambda x: x["score"], reverse=True)
    picked = []
    for ap in cand:
        if len(picked) >= total_k:
            break
        if any(_sim(ap["sentence"], p["sentence"]) >= dedupe_similarity for p in picked):
            continue
        picked.append(ap)
    return picked

# ---- assembly + tiny rewrite (no new facts) ----
def assemble_answer(pieces: List[Dict]) -> Tuple[str, List[Dict]]:
    if not pieces:
        return "I couldn’t find grounded information to answer this precisely.", []
    by_src = {}
    for p in pieces:
        by_src.setdefault(p["source"], []).append(p)
    ordered = sorted(by_src.items(), key=lambda kv: max(x["score"] for x in kv[1]), reverse=True)

    citations, idx_map, idx = [], {}, 1
    sents = []
    for src, items in ordered:
        for it in sorted(items, key=lambda x: x["score"], reverse=True):
            if src not in idx_map:
                idx_map[src] = idx
                citations.append({"idx": idx, "doc_id": it["doc_id"], "source": src})
                idx += 1
            sents.append(f'{it["sentence"]} [{idx_map[src]}]')
    ans = " ".join(sents)
    ans = re.sub(r'\s+\[(\d+)\]\s+\[(\1)\]', r' [\1]', ans)  # merge dup cites
    ans = re.sub(r'\s{2,}', ' ', ans).strip()
    if len(ans) > 900:
        ans = ans[:900].rsplit(' ', 1)[0] + "…"
    return ans, citations

# ---- public API (same name as v1) ----
def generate_answer(query: str, retrieved: List[Dict], total_k: int = 6, max_per_doc: int = 3, do_rewrite: bool = True):
    pieces = select_supporting_sentences(retrieved, query, total_k=total_k, max_per_doc=max_per_doc)
    answer, citations = assemble_answer(pieces)
    return {
        "answer": answer,
        "citations": citations,
        "supporting_sentences": [
            {"text": p["sentence"], "doc_id": p["doc_id"], "source": p["source"], "score": round(p["score"], 4)}
            for p in pieces
        ]
    }

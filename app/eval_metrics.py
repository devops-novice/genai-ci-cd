# app/eval_metrics.py
from typing import List

def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    topk = retrieved[:k]; hits = sum(1 for x in topk if x in relevant)
    return hits / max(1, len(topk))

def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    topk = retrieved[:k]; hits = sum(1 for x in topk if x in relevant)
    return hits / max(1, len(relevant))

def hit_at_k(retrieved: List[str], relevant: List[str], k: int) -> bool:
    return any(x in relevant for x in retrieved[:k])

def mrr(retrieved: List[str], relevant: List[str]) -> float:
    for i, x in enumerate(retrieved, 1):
        if x in relevant: return 1.0 / i
    return 0.0

def exact_match(pred: str, gold: str) -> bool:
    return pred.strip().lower() == gold.strip().lower()

def f1_tokens(pred: str, gold: str) -> float:
    ps, gs = pred.lower().split(), gold.lower().split()
    common = sum(min(ps.count(w), gs.count(w)) for w in set(ps))
    if common == 0: return 0.0
    p = common/len(ps); r = common/len(gs); return 2*p*r/(p+r)

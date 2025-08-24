# app/gen_registry.py
import os
from typing import Callable, Dict, List, Tuple

# v1: current baseline (returns: tuple[str, list[str]])
from app.generator import generate_answer as gen_v1

# v2 core: returns dict; we'll adapt it
from app.generator_v2_multi import generate_answer as gen2_core

def gen_v2_compat(question: str, retrieved: List[dict], cfg: dict | None = None) -> Tuple[str, List[str]]:
    cfg = cfg or {}
    total_k = int(cfg.get("total_k", 6))
    max_per_doc = int(cfg.get("max_per_doc", 3))
    res = gen2_core(query=question, retrieved=retrieved, total_k=total_k, max_per_doc=max_per_doc)
    answer = res["answer"]
    # Convert supporting sentences → used_ids (dedup, keep order)
    ids = []
    for s in res.get("supporting_sentences", []):
        did = s.get("doc_id")
        if did and did not in ids:
            ids.append(did)
    return answer, ids

_REGISTRY: Dict[str, Callable] = {
    "v1": gen_v1,          # unchanged
    "v2": gen_v2_compat,   # drop-in compatible with rag_engine
}

def get_generator(name: str | None = None) -> Callable:
    key = (name or os.getenv("GEN_VERSION") or "v1").lower()
    return _REGISTRY.get(key, gen_v1)


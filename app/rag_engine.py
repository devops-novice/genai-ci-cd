# app/rag_engine.py
from __future__ import annotations
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel

from .guardrails import validate_input, filter_retrieved
from app.retrieval import retrieve_topk
from app.gen_registry import get_generator  # v1 (baseline) | v2 (multi-sentence)

# -----------------------------
# Public response schema used by your API
# -----------------------------
class RAGResponse(BaseModel):
    answer: str
    sources: List[str]   # e.g., filenames/URLs of used chunks (deduped, order-preserving)
    chunks: List[str]    # the TEXT of the chunks actually used to form the answer


# -----------------------------
# Internal pipeline runner
# -----------------------------
def _run_pipeline(
    question: str,
    k: int = 5,
    run_config: Optional[dict] = None
) -> Tuple[str, List[str], List[Dict]]:
    """
    Returns (answer, used_ids, retrieved)
    - retrieved: list of dicts [{"id":..., "text":..., "source":..., "score":...}, ...]
    - used_ids: IDs of chunks the generator actually used (order preserved)
    """
    ok, reason = validate_input(question)
    if not ok:
        # Keep behavior predictable for callers; raise or return a safe tuple.
        return f"Rejected by guardrail: {reason}", [], []

    run_config = run_config or {}

    # 1) Retrieve and guard
    retrieved: List[Dict] = retrieve_topk(question, k=k, cfg=run_config.get("retriever", {}))
    retrieved = filter_retrieved(retrieved)  # domain/source allowlist

    # 2) Generate (switchable v1/v2)
    gen_cfg = (run_config.get("generator", {}) if run_config else {}) or {}
    version = gen_cfg.get("version")  # "v1" | "v2" | None
    generator = get_generator(version)  # env GEN_VERSION also supported inside registry
    answer, used_ids = generator(question, retrieved, cfg=gen_cfg)

    return answer, used_ids, retrieved


# -----------------------------
# High-level: produce API response
# -----------------------------
def rag_with_sources(
    question: str,
    k: int = 5,
    run_config: Optional[dict] = None
) -> RAGResponse:
    """
    Runs the pipeline and returns a RAGResponse that your FastAPI route can serialize.
    """
    answer, used_ids, retrieved = _run_pipeline(question, k=k, run_config=run_config)

    # Build sources and chunks from the retrieved items we actually used
    idset = set(used_ids)
    sources: List[str] = []
    chunks: List[str] = []
    seen_src: set[str] = set()

    for r in retrieved:
        rid = r.get("id") or r.get("doc_id")
        if rid in idset:
            txt = r.get("text") or r.get("page_content") or ""
            if txt:
                chunks.append(txt)
            src = r.get("source") or r.get("file") or "local"
            if src not in seen_src:
                sources.append(src)
                seen_src.add(src)

    return RAGResponse(answer=answer, sources=sources, chunks=chunks)


# -----------------------------
# Evaluation helpers
# -----------------------------
from .eval_metrics import precision_at_k, recall_at_k, hit_at_k, mrr, exact_match, f1_tokens
from .faithfulness import check_faithfulness

def evaluate_rag(
    question: str,
    gold_answer: str,
    expected_source_ids: List[str],
    k: int = 5,
    run_config: Optional[dict] = None
) -> Dict:
    """
    Runs retrieval + generation, then computes retrieval/generation/faithfulness metrics.
    Returns a dict suitable for logs or an eval endpoint.
    """
    answer, used_ids, retrieved = _run_pipeline(question, k=k, run_config=run_config)

    r_ids = [r.get("id") or r.get("doc_id") for r in retrieved]

    retrieval = {
        "k": k,
        "hit_at_k": hit_at_k(r_ids, expected_source_ids, k),
        "precision_at_k": precision_at_k(r_ids, expected_source_ids, k),
        "recall_at_k": recall_at_k(r_ids, expected_source_ids, k),
        "mrr": mrr(r_ids, expected_source_ids),
        "retrieved_ids": r_ids,
        "used_ids": used_ids,
    }
    generation = {
        "exact_match": exact_match(answer, gold_answer),
        "f1": f1_tokens(answer, gold_answer),
    }
    faithfulness = check_faithfulness(answer, retrieved, expected_source_ids)

    return {
        "retrieval": retrieval,
        "generation": generation,
        "faithfulness": faithfulness,
        "answer": answer,
    }


# -----------------------------
# Optional wrapper class (keeps old call sites working)
# -----------------------------
class RAGEngine:
    """
    Backward-compatible wrapper.
    If older code did: `RAGEngine(k=3).query("...")`, it will still work and
    return a RAGResponse.
    """
    def __init__(self, k: int = 5):
        self.k = k

    def query(self, question: str, run_config: Optional[dict] = None) -> RAGResponse:
        return rag_with_sources(question, k=self.k, run_config=run_config)

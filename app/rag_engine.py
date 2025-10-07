# app/rag_engine.py
from __future__ import annotations

from typing import List, Dict, Tuple, Optional
from pathlib import Path
import os

from app.log_utils import log_event
from .guardrails import validate_input, filter_retrieved
from app.gen_registry import get_generator

# IMPORTANT: we import the API models from a single place to avoid duplication/mismatch
from app.schemas import RAGResponse, Citation

# Retrieval entry point. This must exist.
# Tip: if your current app/retrieval.py doesn't expose retrieve_topk,
# add a tiny alias there that returns a list of dicts OR (score, payload) tuples.
from app.retrieval import retrieve_topk


# -----------------------------
# Helpers
# -----------------------------
def _normalize_retrieved(raw: List) -> List[Dict]:
    """
    Accepts retrieval in one of two shapes (we normalize both):
      1) List[Dict] like:
         {"id": "...", "doc_id": "...", "chunk_id": "...", "text": "...",
          "source": "docs/file.md", "title": "Human Title", "score": 0.12}
      2) List[Tuple[score: float, payload: Dict]] where payload has keys above.

    Returns a normalized list of dicts with keys:
      id, doc_id, chunk_id, text, source, title, source_path, score
    """
    out: List[Dict] = []
    for item in raw:
        if isinstance(item, tuple) and len(item) == 2:
            score, payload = item
            r = dict(payload)
            r["score"] = float(score)
        elif isinstance(item, dict):
            r = dict(item)
        else:
            # Unknown shape; best-effort wrap
            r = {"text": str(item), "score": 0.0}

        # Unify fields / fallbacks
        doc_id = r.get("doc_id") or r.get("id") or ""
        src = r.get("source") or r.get("source_path") or r.get("file") or ""
        title = r.get("title") or (Path(src).stem if src else doc_id) or "local"

        out.append({
            "id": r.get("id") or doc_id,
            "doc_id": doc_id,
            "chunk_id": r.get("chunk_id") or f"{doc_id}_0000",
            "text": r.get("text") or r.get("page_content") or "",
            "source": src,
            "title": title,
            "source_path": src,      # keep both for callers
            "score": float(r.get("score", 0.0)),
        })
    return out


def _build_citations(
    retrieved_norm: List[Dict],
    used_ids: List[str]
) -> Tuple[List[str], List[str], List[Citation]]:
    """
    Build (sources, chunks, citations) from normalized retrieval + the generator's used_ids.
    - sources: unique list of human-readable sources (legacy)
    - chunks : TEXT of used chunks (legacy)
    - citations: structured objects for the new API
    """
    idset = set(used_ids)
    sources: List[str] = []
    chunks: List[str] = []
    citations: List[Citation] = []
    seen_src: set[str] = set()
    idx = 1

    for r in retrieved_norm:
        rid = r["id"] or r["doc_id"]
        if rid in idset:
            # legacy chunks list
            if r["text"]:
                chunks.append(r["text"])

            # legacy sources list (dedup, order-preserving)
            src = r["title"] or r["source_path"] or r["source"] or r["doc_id"] or "local"
            if src not in seen_src:
                sources.append(src)
                seen_src.add(src)

            # structured citation
            citations.append(Citation(
                idx=idx,
                source=src,
                doc_id=r["doc_id"] or rid,
                # optional enriched fields — present if your retriever provided them
                **{
                    "chunk_id": r.get("chunk_id"),
                    "title": r.get("title"),
                    "source_path": r.get("source_path"),
                }
            ))
            idx += 1

    # If the generator returned no used_ids (some v1 generators), fall back to first-seen order
    if not used_ids and not citations and retrieved_norm:
        seen_src.clear()
        idx = 1
        for r in retrieved_norm:
            src = r["title"] or r["source_path"] or r["source"] or r["doc_id"] or "local"
            if src not in seen_src:
                sources.append(src)
                seen_src.add(src)
                citations.append(Citation(
                    idx=idx,
                    source=src,
                    doc_id=r["doc_id"] or r["id"] or "",
                    chunk_id=r.get("chunk_id"),
                    title=r.get("title"),
                    source_path=r.get("source_path"),
                ))
                if r["text"]:
                    chunks.append(r["text"])
                idx += 1

    return sources, chunks, citations


# -----------------------------
# Internal pipeline runner
# -----------------------------
def _run_pipeline(
    question: str,
    k: int = 5,
    run_config: Optional[dict] = None
) -> Tuple[str, List[str], List[Dict], List[Dict]]:
    """
    Returns (answer, used_ids, retrieved_norm, citations_raw)
      - retrieved_norm: normalized retrieval dicts (see _normalize_retrieved)
      - used_ids: IDs of chunks the generator actually used (order preserved)
      - citations_raw: (optional) structured citations from generator v2 (idx/source/doc_id/…)
    """
    ok, reason = validate_input(question)
    if not ok:
        # Keep behavior predictable; do not raise in HTTP path.
        return f"Rejected by guardrail: {reason}", [], [], []

    run_config = run_config or {}

    # 1) Retrieve (allow run_config override for k) + guardlist filters
    r_cfg = (run_config.get("retriever", {}) if run_config else {}) or {}
    k_eff = int(r_cfg.get("k", k))
    retrieved_raw: List = retrieve_topk(question, k=k_eff, cfg=r_cfg)
    retrieved_raw = filter_retrieved(retrieved_raw)   # domain/source allowlist
    retrieved_norm = _normalize_retrieved(retrieved_raw)

    # 2) Generate (switchable v1/v2)
    gen_cfg = (run_config.get("generator", {}) if run_config else {}) or {}
    version = gen_cfg.get("version")  # "v1" | "v2" | None; env GEN_VERSION also supported in registry
    generator = get_generator(version)
    result = generator(question, retrieved_norm, cfg=gen_cfg)

    answer: str
    used_ids: List[str]
    citations_raw: List[Dict] = []

    # v1 returns (answer, used_ids); v2 returns (answer, used_ids, citations_raw)
    if isinstance(result, tuple) and len(result) == 3:
        answer, used_ids, citations_raw = result
    else:
        answer, used_ids = result

    return answer, used_ids, retrieved_norm, citations_raw


# -----------------------------
# High-level: produce API response
# -----------------------------
def rag_with_sources(
    question: str,
    k: int = 5,
    run_config: Optional[dict] = None
) -> RAGResponse:
    """
    Runs the pipeline and returns a RAGResponse compatible with app.schemas.RAGResponse.
    Keeps legacy fields (sources/chunks) and adds structured citations.
    """
    answer, used_ids, retrieved_norm, citations_raw = _run_pipeline(
        question, k=k, run_config=run_config
    )

    # If generator already produced citations (v2), trust them.
    citations: List[Citation] = []
    if citations_raw:
        for c in citations_raw:
            citations.append(Citation(
                idx=int(c.get("idx")),
                source=c.get("source", "local"),
                doc_id=c.get("doc_id", ""),
                chunk_id=c.get("chunk_id"),
                title=c.get("title"),
                source_path=c.get("source_path"),
            ))
        # Build legacy sources/chunks aligned to provided citations
        sources = [c.source for c in sorted(citations, key=lambda x: x.idx)]
        # For legacy chunks, map by doc_id/chunk_id from retrieved_norm in citation order
        chunks_map = {(r["doc_id"], r["chunk_id"]): r["text"] for r in retrieved_norm}
        chunks = [
            chunks_map.get((c.doc_id, c.chunk_id), "")
            for c in sorted(citations, key=lambda x: x.idx)
            if c.chunk_id
        ]
    else:
        # Derive citations + legacy fields from normalized retrieval + used_ids
        sources, chunks, citations = _build_citations(retrieved_norm, used_ids)

    # Minimal, audit-friendly log (never break the response on logging issues)
    try:
        version = ((run_config or {}).get("generator", {}) or {}).get("version") \
                  or os.getenv("GEN_VERSION") or "v1"
        r_cfg = ((run_config or {}).get("retriever", {}) or {})
        k_eff = int(r_cfg.get("k", k))
        log_event("rag.answer", {
            "version": version,
            "k": k_eff,
            "used_ids": used_ids,
            "sources": sources,
            "question_len": len(question),
            "answer_len": len(answer),
        })
    except Exception:
        pass

    # Backward-compatible response (sources/chunks) + structured citations
    return RAGResponse(
        answer=answer,
        sources=sources,           # legacy (kept)
        chunks=chunks,             # legacy (kept)
        citations=citations,       # new, structured
    )


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
    answer, used_ids, retrieved_norm, _ = _run_pipeline(question, k=k, run_config=run_config)

    r_ids = [r.get("id") or r.get("doc_id") for r in retrieved_norm]

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
    faithfulness = check_faithfulness(answer, retrieved_norm, expected_source_ids)

    return {
        "retrieval": retrieval,
        "generation": generation,
        "faithfulness": faithfulness,
        "answer": answer,
    }


# -----------------------------
# Optional wrapper (keeps old call sites working)
# -----------------------------
class RAGEngine:
    """
    Back-compatible wrapper.
    If older code did: `RAGEngine(k=3).query("...")`, it still returns a RAGResponse.
    """
    def __init__(self, k: int = 5):
        self.k = k

    def query(self, question: str, run_config: Optional[dict] = None) -> RAGResponse:
        return rag_with_sources(question, k=self.k, run_config=run_config)

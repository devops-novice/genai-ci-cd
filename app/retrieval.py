# app/retrieval.py
from __future__ import annotations

from typing import List, Tuple, Dict, Any
from pathlib import Path

# FAISS loader (works with faiss_index/index.faiss + index.pkl)
try:
    from langchain_community.vectorstores import FAISS
except Exception:
    from langchain.vectorstores import FAISS

from app.embedding_utils import get_embedder


class NoOpReranker:
    def rerank(self, query: str, candidates, k: int):
        return candidates[:k]


# app/retrieval.py
def _load_vs():
    emb = get_embedder()
    vs = FAISS.load_local("faiss_index", emb, allow_dangerous_deserialization=True)
    try:
        d_idx = vs.index.d
        d_emb = len(emb.embed_query("probe"))
        if d_idx != d_emb:
            raise RuntimeError(
                f"Embedding dim mismatch: index={d_idx} vs embedder={d_emb}. "
                f"Delete faiss_index/ and rebuild with scripts.embed_and_store using the current embedder."
            )
    except Exception:
        # if anything goes wrong in the check, just return vs; FAISS will error anyway
        pass
    return vs


def retrieve_topk(query: str, k: int = 6, cfg: Dict[str, Any] | None = None) -> List[Tuple[float, Dict]]:
    """
    Unified retrieval facade used by rag_engine.
    Returns a list of (score, payload) where payload has:
      id, doc_id, chunk_id, text, source, title, source_path
    """
    vs = _load_vs()
    docs_scores = vs.similarity_search_with_score(query, k=k)
    out: List[Tuple[float, Dict]] = []
    for doc, score in docs_scores:
        md = doc.metadata or {}
        payload = {
            "id": f"{md.get('doc_id','')}/{md.get('chunk_id','')}",
            "doc_id": md.get("doc_id") or Path(md.get("source", "")).stem or "unknown",
            "chunk_id": md.get("chunk_id", "unknown_0000"),
            "text": doc.page_content,
            "source": md.get("source") or "",
            "title": md.get("title") or md.get("doc_id") or "",
            "source_path": md.get("source") or "",
        }
        out.append((float(score), payload))
    return out


# Back-compat alias (if any old code imported this name)
def retrieve(query: str, k: int = 6) -> List[Tuple[float, Dict]]:
    return retrieve_topk(query, k=k)


__all__ = ["retrieve_topk", "retrieve", "NoOpReranker"]

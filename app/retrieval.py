# app/retrieval.py
from typing import List, Dict, Optional
from .embedding_utils import get_retriever

def retrieve_topk(question: str, k: int = 5, cfg: Optional[dict] = None) -> List[Dict]:
    """
    Wrap LangChain retriever -> returns a list of dicts:
    [{"id": "<file.md#chunkN>", "text": "...", "source": "<file.md>"}]
    """
    cfg = cfg or {}
    index_path = cfg.get("index_path", "faiss_index")
    flt = cfg.get("filters")  # e.g., {"source": "some_file.md"}

    retriever = get_retriever(index_path=index_path, k=k, filters=flt)
    docs = retriever.invoke(question)  # List[Document]

    results: List[Dict] = []
    for d in docs:
        meta = d.metadata or {}
        # Prefer deterministic IDs stamped during chunking
        chunk_id = (
            meta.get("id")
            or meta.get("chunk_id")
            or f"{meta.get('source', 'unknown')}#{hash(d.page_content) & 0xffff}"
        )
        results.append({
            "id": chunk_id,
            "text": d.page_content,
            "source": meta.get("source", "unknown"),
        })

    return results

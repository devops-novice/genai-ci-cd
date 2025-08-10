# uses your existing get_retriever() from app.embedding_utils
from typing import List, Dict, Tuple
from .embedding_utils import get_retriever

def retrieve_topk(question: str, k: int = 5, cfg: dict | None = None) -> List[Dict]:
    """
    Wraps LangChain retriever -> returns [{'id', 'text', 'source'}] for our evaluator.
    """
    cfg = cfg or {}
    index_path = cfg.get("index_path", "faiss_index")
    flt = cfg.get("filters")  # e.g., {"source": "some_file.md"}

    retriever = get_retriever(index_path=index_path, k=k, filters=flt)
    docs = retriever.invoke(question) #retriever.get_relevant_documents(question)  # List[Document]

    results = []
    for d in docs:
        meta = d.metadata or {}
        # Prefer a stable chunk id if present; else fall back to source name + char span
        chunk_id = meta.get("chunk_id") or f"{meta.get('source','unknown')}#{hash(d.page_content) & 0xffff}"
        results.append({
            "id": chunk_id,
            "text": d.page_content,
            "source": meta.get("source", "unknown")
        })
    return results

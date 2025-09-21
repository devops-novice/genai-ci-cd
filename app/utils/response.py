# app/utils/response.py
from typing import Any, Dict, List

def _doc_to_chunk(doc: Any) -> Dict[str, Any]:
    # Support: LlamaIndex / LangChain / plain dict / string
    if isinstance(doc, dict):
        # already dict-ish
        source = doc.get("source") or doc.get("metadata", {}).get("source") or ""
        content = doc.get("content") or doc.get("page_content") or ""
        out = dict(doc)
        out.setdefault("source", source)
        out.setdefault("content", content)
        return out

    # LangChain Document
    if hasattr(doc, "page_content"):
        meta = getattr(doc, "metadata", {}) or {}
        return {
            "source": meta.get("source") or meta.get("file_name") or "",
            "content": doc.page_content,
            **({k: v for k, v in meta.items() if k not in ("source", "file_name")} or {})
        }

    # Plain string fallback
    if isinstance(doc, str):
        return {"source": "", "content": doc}

    # Last resort
    return {"source": "", "content": str(doc)}

def to_chunks(docs: List[Any]) -> List[Dict[str, Any]]:
    return [ _doc_to_chunk(d) for d in (docs or []) ]

def to_sources(chunks: List[Dict[str, Any]]) -> List[str]:
    return sorted({ (c.get("source") or "").strip() for c in (chunks or []) if c.get("source") })

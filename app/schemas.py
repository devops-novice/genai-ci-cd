# app/schemas.py
from __future__ import annotations

from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field


# -------------------------
# General/legacy schemas
# -------------------------
class Analysis(BaseModel):
    summary: str
    tone: str


class ReasoningOutput(BaseModel):
    reasoning: str
    conclusion: str


# Canonical request model used by /rag-real and others
# - Keeps legacy `config` blob
# - Adds optional `top_k` and `mode` controls
class PromptRequest(BaseModel):
    prompt: str
    config: Optional[Dict[str, Any]] = None
    top_k: Optional[int] = None
    mode: Optional[Literal["merged", "per_doc"]] = None


# -------------------------
# RAG response & helpers
# -------------------------
# Structured citation (new)
class Citation(BaseModel):
    idx: int
    source: str
    doc_id: str
    # Optional enrichments (present when available)
    chunk_id: Optional[str] = None
    title: Optional[str] = None
    source_path: Optional[str] = None


# Retrieval diagnostics (optional)
class RetrievalDebug(BaseModel):
    mode: Literal["merged", "per_doc"]
    top_k: int
    used_reranker: bool
    fusion: Optional[str] = None  # e.g., "rrf" or None


# Backward-compatible RAG response
# - Keeps legacy fields (sources/chunks)
# - Adds structured citations and retrieval debug
class RAGResponse(BaseModel):
    answer: str
    # Legacy fields (keep to avoid breaking existing clients)
    sources: Optional[List[str]] = Field(default_factory=list)
    chunks: Optional[List[str]] = Field(default_factory=list)
    # New fields
    citations: Optional[List[Citation]] = None
    retrieval: Optional[RetrievalDebug] = None


# -------------------------
# Highlighting/debug flows
# -------------------------
class Highlight(BaseModel):
    term: str
    start_index: int
    end_index: int


class HighlightedChunk(BaseModel):
    source: str
    content: str
    highlights: List[Highlight]


class RAGWithHighlightsResponse(BaseModel):
    answer: str
    highlighted_chunks: List[HighlightedChunk]


class RetrievedChunk(BaseModel):
    id: Optional[str] = None
    source: str
    content: str
    score: Optional[float] = None
    start: Optional[int] = None
    end: Optional[int] = None


class DebugResponse(BaseModel):
    query: str
    answer: str
    sources: List[str]
    chunks: List[RetrievedChunk]
    meta: Optional[Dict[str, Any]] = None


# Minimal request alias used elsewhere
class Query(BaseModel):
    prompt: str

# app/schemas.py

from pydantic import BaseModel
from typing import Optional, Dict, List, Any


class Analysis(BaseModel):
    summary: str
    tone: str

# app/schemas.py

class ReasoningOutput(BaseModel):
    reasoning: str
    conclusion: str


class PromptRequest(BaseModel):
    prompt: str
    config: Optional[Dict] = None  # ✅ e.g., {"filters": {"source": "AI_Leadership_Reading_Plan_Refined.md"}, "k": 5}

# define Citation **before** RAGResponse
class Citation(BaseModel):
    idx: int
    source: str
    doc_id: str

class RAGResponse(BaseModel):
    answer: str
    sources: List[str]
    chunks: List[str]
    citations: Optional[List[Citation]] = None


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

class Query(BaseModel):
    prompt: str  # keep 'prompt' as the canonical input

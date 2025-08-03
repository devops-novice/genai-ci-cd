# app/schemas.py

from pydantic import BaseModel
from typing import Optional, Dict, List
from pydantic import BaseModel

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


class RAGResponse(BaseModel):
    answer: str
    sources: List[str]
    chunks: List[str]

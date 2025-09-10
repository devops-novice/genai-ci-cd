# app/rag_router.py
from fastapi import APIRouter, Body, Query, HTTPException
from app.rag_engine import rag_with_sources, RAGResponse

router = APIRouter()

@router.post("/rag-with-sources", response_model=RAGResponse)
def rag_with_sources_route(payload: dict = Body(...), gen: str | None = Query(None, pattern="^(v1|v2)$")):
    prompt = payload.get("prompt") or payload.get("query")
    if not prompt:
        raise HTTPException(status_code=422, detail="Field 'prompt' is required")
    run_cfg = {"generator": {"version": gen}} if gen else {}
    return rag_with_sources(prompt, k=5, run_config=run_cfg)

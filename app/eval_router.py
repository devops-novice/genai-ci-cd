from fastapi import APIRouter
from pydantic import BaseModel
from .rag_engine import evaluate_rag

router = APIRouter()

class EvalRequest(BaseModel):
    question: str
    ground_truth_answer: str
    expected_source_ids: list[str]
    k: int = 5
    run_config: dict = {}

@router.post("/evaluate-rag")
def evaluate_rag_route(req: EvalRequest):
    return evaluate_rag(
        question=req.question,
        gold_answer=req.ground_truth_answer,
        expected_source_ids=req.expected_source_ids,
        k=req.k,
        run_config=req.run_config
    )

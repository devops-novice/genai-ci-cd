# Week 5 Reflection – AI Transformation Journey

## **August 4, 2025 — Day 1 Reflection**

### **Focus**
Built and tested the `/evaluate-rag` endpoint with retrieval & generation metrics, faithfulness check, and an automated evaluation runner over a golden set.

---

### **What I Did Today**
- Implemented retrieval (`retrieve_topk`) and deterministic generation (`generate_answer`) stubs.
- Added metrics:
  - `precision@k`
  - `recall@k`
  - `MRR`
  - `Exact Match`
  - `F1`
  - `faithfulness`
- Built a golden set with 9 Q/A pairs in `docs/golden_set/rag_qa.jsonl`.
- Created `scripts/run_eval.py` to score the golden set and output:
  - `summary.json`
  - `cases.csv`

---

### **Metrics Snapshot**
From `docs/golden_set/outputs/summary.json`:
```json
{
  "n": 9,
  "precision_at_k": 0.0,
  "recall_at_k": 0.0,
  "mrr": 0.0,
  "f1": 0.183,
  "faithfulness_supported_rate": 0.0
}

# scripts/daily_eval_snapshot.py
from __future__ import annotations
import os, json, datetime, pathlib
from typing import List, Dict

# Allow `import app.*` when run as a script
import sys
sys.path.insert(0, os.getcwd())

from app.rag_engine import evaluate_rag  # uses your in-process pipeline

DATA_CANDIDATES = [
    "docs/golden_set.jsonl",
    "docs/golden.jsonl",
    "docs/gold.jsonl",
]

def load_dataset() -> List[Dict]:
    for p in DATA_CANDIDATES:
        if os.path.exists(p):
            out = []
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        out.append(json.loads(line))
            return out
    # Fallback minimal example so the script always runs
    return [{
        "id": "ex1",
        "question": "What is RAG?",
        "ground_truth_answer": "Retrieval-augmented generation combines retrieval and generation to produce grounded answers.",
        "expected_source_ids": []  # leave empty if you don't track expected IDs
    }]

def run_eval(label: str, dataset: List[Dict], gen_version: str) -> Dict:
    rows = []
    for ex in dataset:
        metrics = evaluate_rag(
            question=ex["question"],
            gold_answer=ex.get("ground_truth_answer", ""),
            expected_source_ids=ex.get("expected_source_ids", []),
            k=5,
            run_config={"generator": {"version": gen_version}},
        )
        rows.append({
            "id": ex.get("id"),
            "f1": metrics["generation"]["f1"],
            "exact_match": metrics["generation"]["exact_match"],
            "retrieval": metrics["retrieval"],
        })
    macro_f1 = sum(r["f1"] for r in rows) / max(1, len(rows))
    return {"label": label, "macro_f1": macro_f1, "rows": rows}

def main():
    today = datetime.date.today().isoformat()
    out_dir = pathlib.Path(f"docs/eval/{today}")
    out_dir.mkdir(parents=True, exist_ok=True)

    ds = load_dataset()

    v1 = run_eval("v1", ds, "v1")
    v2 = run_eval("v2", ds, "v2")

    (out_dir / "v1.json").write_text(json.dumps(v1, indent=2), encoding="utf-8")
    (out_dir / "v2.json").write_text(json.dumps(v2, indent=2), encoding="utf-8")

    delta = v2["macro_f1"] - v1["macro_f1"]
    diff = f"""# Eval snapshot — {today}
Macro F1: v1={v1['macro_f1']:.3f} → v2={v2['macro_f1']:.3f} (Δ={delta:+.3f})

Dataset size: {len(ds)}
Generator settings: via run_config (v1 vs v2)
"""
    (out_dir / "diff.md").write_text(diff, encoding="utf-8")
    print(diff)

if __name__ == "__main__":
    main()

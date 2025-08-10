import json, csv, statistics as stats
from pathlib import Path
from app.rag_engine import evaluate_rag

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT/"docs/golden_set/rag_qa.jsonl"
OUT  = ROOT/"docs/golden_set/outputs"
OUT.mkdir(parents=True, exist_ok=True)

def main(k=5):
    cases = []
    with open(GOLD) as f:
        for line in f:
            ex = json.loads(line)
            res = evaluate_rag(
                question=ex["question"],
                gold_answer=ex["answer"],
                expected_source_ids=ex["source_ids"],
                k=k,
                run_config={"retriever":{"index_path":"faiss_index"}}
            )
            cases.append({
                "id": ex["id"],
                "p_at_k": res["retrieval"]["precision_at_k"],
                "r_at_k": res["retrieval"]["recall_at_k"],
                "mrr": res["retrieval"]["mrr"],
                "em": res["generation"]["exact_match"],
                "f1": res["generation"]["f1"],
                "faith_supported": res["faithfulness"]["supported"],
                "retrieved_ids": "|".join(res["retrieval"]["retrieved_ids"])
            })

    summary = {
        "n": len(cases),
        "precision_at_k": round(stats.mean(c["p_at_k"] for c in cases), 3),
        "recall_at_k": round(stats.mean(c["r_at_k"] for c in cases), 3),
        "mrr": round(stats.mean(c["mrr"] for c in cases), 3),
        "f1": round(stats.mean(c["f1"] for c in cases), 3),
        "faithfulness_supported_rate": round(sum(1 for c in cases if c["faith_supported"]) / len(cases), 3)
    }

    (OUT/"summary.json").write_text(json.dumps(summary, indent=2))
    with open(OUT/"cases.csv","w", newline="") as c:
        w = csv.DictWriter(c, fieldnames=list(cases[0].keys()))
        w.writeheader(); w.writerows(cases)

    # Starter thresholds (we’ll tighten later)
    failures = []
    if summary["recall_at_k"] < 0.60: failures.append("recall@k<0.60")
    if summary["faithfulness_supported_rate"] < 0.80: failures.append("faithfulness<0.80")
    if failures: (OUT/"SUMMARY_FAILED").write_text("\n".join(failures))

if __name__ == "__main__":
    main()

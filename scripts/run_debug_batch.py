#!/usr/bin/env python3
import argparse, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

QUERIES = [
    "Why did our retrieval originally return only one result, and what exact change fixed it?",
    "What problem do stable chunk IDs solve in the golden set evaluation pipeline?",
    "Explain how highlighted_chunks in /rag-with-highlights improves UX for debugging faithfulness.",
    "If Top-K=5, 3 of 5 are relevant but there are 10 total relevant chunks, what are precision@k and recall@k, and why do they matter?",
    "Why can F1 be low while faithfulness is high in our pipeline? Give one concrete repo example.",
    "List all implemented RAG endpoints and describe their response structure and intended use.",
    "What are the main RAG failure modes we track (retrieval, grounding, hallucination, evaluation) and how do we label them in logs?",
    "Which piece of code enforces the 'abstain/I don’t know' behavior, and when should the model abstain?",
    "What chunk schema do we use (fields and purpose), and how are chunk IDs generated to remain stable across runs?",
    "What was the JSON decode error we saw earlier, why did it occur, and how should clients format requests to avoid it?"
]

def post_json(url: str, payload: dict, timeout: float = 20.0) -> tuple[int, dict | str]:
    body = json.dumps(payload).encode("utf-8")
    req = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
            return resp.getcode(), json.loads(data)
    except HTTPError as e:
        try:
            err = e.read().decode("utf-8")
        except Exception:
            err = str(e)
        return e.code, err
    except URLError as e:
        return 0, f"URLError: {e.reason}"
    except Exception as e:
        return 0, f"Error: {e}"

def main():
    ap = argparse.ArgumentParser(description="Batch-run /rag-debug prompts and save a markdown report.")
    ap.add_argument("--url", default=os.environ.get("RAG_DEBUG_URL", "http://localhost:8000/rag-debug"),
                    help="rag-debug endpoint URL")
    ap.add_argument("--out", default="docs/evaluation_errors_today.md",
                    help="output markdown path")
    ap.add_argument("--workers", type=int, default=6,
                    help="number of concurrent workers")
    args = ap.parse_args()

    url = args.url
    began = time.strftime("%Y-%m-%d %H:%M:%S")
    results = [None] * len(QUERIES)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(post_json, url, {"prompt": q}): (i, q) for i, q in enumerate(QUERIES)}
        for fut in as_completed(futs):
            i, q = futs[fut]
            code, data = fut.result()
            results[i] = (q, code, data)

    # Print a compact table to stdout
    print("\n=== /rag-debug batch ===")
    for i, (q, code, data) in enumerate(results, 1):
        ok = (code == 200 and isinstance(data, dict) and
              "answer" in data and "sources" in data and "chunks" in data)
        sources = ", ".join((data.get("sources") or [])[:2]) if isinstance(data, dict) else ""
        ch_cnt = len(data.get("chunks") or []) if isinstance(data, dict) else 0
        print(f"{i:02d}. {('OK' if ok else 'ERR')} [{code}]  chunks={ch_cnt:02d}  sources={sources}")

    # Write full markdown with placeholders for Error Type/Notes
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(f"# Evaluation Errors – {time.strftime('%Y-%m-%d')}\n")
        f.write(f"_Generated: {began}_\n\n")
        for i, (q, code, data) in enumerate(results, 1):
            f.write(f"## Query {i}\n")
            f.write(f"- **Question**: {q}\n")
            if code == 200 and isinstance(data, dict):
                ans = (data.get("answer") or "").strip()
                srcs = data.get("sources") or []
                chunks = data.get("chunks") or []
                # Keep chunks brief in md to keep file readable (avoid backslashes inside f-strings)
                preview_lines = []
                for c in chunks[:3]:
                    text = str(c).replace("\n", " ")[:180]
                    preview_lines.append(f"  - {text}")
                preview = "\n".join(preview_lines)

                f.write(f"- **Answer**: {ans}\n")
                f.write(f"- **Sources**: {', '.join(srcs)}\n")
                f.write("- **Chunks (preview)**:\n")
                f.write(preview + "\n" if preview else "  - (none)\n")
                f.write("- **Error Type**: Retrieval / Grounding / Hallucination / Evaluation\n")
                f.write("- **Notes**: \n\n")
            else:
                f.write(f"- **ERROR**: HTTP {code} – {data}\n\n")

    print(f"\nSaved detailed report → {args.out}")

if __name__ == "__main__":
    sys.exit(main())

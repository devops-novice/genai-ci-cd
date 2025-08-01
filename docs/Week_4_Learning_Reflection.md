# 🧠 Week 4 Learning Reflection (July 28 – August 3, 2025)

This reflection summarizes the core engineering and conceptual progress made in Week 4 of the AI Upskilling Journey.

---

## ✅ What I Did This Week

- 📦 Modularized `RAGEngine` class for reusability
- 🧪 Wrote and passed unit tests using `pytest`
- 🔧 Fixed FastAPI imports and packaging issues
- 🖥️ Built `rag_cli.py` to enable command-line querying
- 🗂️ Added optional `--source` filter for scoped retrieval
- 📜 Updated `.gitignore`, committed clean logs
- 📚 Finalized dual-book reading plan for Aug–Mar and committed to GitHub

---

## 🧠 What I Learned

| Trait Practiced                     | What It Trains Me For                                        |
|------------------------------------|---------------------------------------------------------------|
| Modular design via `RAGEngine`     | Building scalable, testable AI infrastructure                |
| CLI-first thinking                 | Empowering devs with flexible access without full APIs        |
| Filtered retrieval (by source)     | Enterprise-grade control over context visibility              |
| Pydantic output schema             | Contract-first mindset for interfacing with UIs or systems    |
| Git discipline                     | Versioned learning, structure hygiene, and traceability       |

---

## 🔍 Reflections

- Reusability is not a bonus — it’s the baseline for scaling AI systems.
- CLI helped me internalize the flow much faster than Swagger ever could.
- By doing source filtering, I got a better feel for how multi-tenant RAGs will work in future enterprise use cases.
- Book alignment helps keep my daily tasks mentally "zoomed out."

---

## ⏭️ Next Up (Friday to Sunday)

- Build an `eval_annotator.py` to label my RAG logs
- Enforce `RAGResponse` schema in all endpoints
- Write a README for this RAG project
- Final retrospective on Week 4 progress


🧠 Friday, August 1 – Manual Evaluation & Ground Truth Logging
✅ What I Did
Built eval_annotator.py to review and annotate RAG outputs manually

Labeled entries for correctness and hallucination

Updated rag_eval_log.jsonl with structured judgment metadata

🧠 What I Learned
Skill Practiced	What It Trains Me For
Ground truth logging	Foundation for LLM benchmarking and real-world eval frameworks
Human-in-the-loop annotation	Replaces guesswork with auditability and precision
Schema-first logging discipline	Enables comparison across runs, versions, and prompt changes
CLI-first developer tooling	Realistic internal DevEx-style RAG evaluation loop

🔭 Reflection
What gets measured, gets improved. Having was_correct and hallucinated flags changes how I view “good enough” answers.

It’s tempting to eyeball responses and move on — this discipline forces me to take a QA lens, not just a dev lens.

I now see how enterprise RAG systems evolve through data-driven iteration, not just prompt tweaking.

⏱️ Time Spent: ~90 minutes

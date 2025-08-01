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

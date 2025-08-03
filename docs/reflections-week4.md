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


---

### 📅 Saturday, August 2 – API Contracting + Documentation

#### ✅ What I Did
- Created a shared `RAGResponse` schema and enforced it across all `/rag-*` API endpoints
- Cleaned and validated response format for FastAPI Swagger UI
- Wrote a dedicated `README_rag_module.md` covering RAG architecture, CLI, logs, and usage
- Committed all work to GitHub as a portfolio-ready deliverable

#### 🧠 What I Learned

| Practice                     | What It Trains Me For                                         |
|------------------------------|---------------------------------------------------------------|
| API schema enforcement       | Stability in interfaces and auditability of AI responses      |
| Contract-first development   | Building integrations others can rely on                      |
| Documentation discipline     | Communication clarity and open-source readiness               |
| CLI + API dual interface     | Supporting different developer workflows without code forks   |

#### 🔭 Reflection
- Swagger UI is only as useful as the schema behind it — response_model gives it life.
- Writing the README helped surface how modular and product-ready this system really is.
- The CLI and API now feel equally strong — that’s intentional developer experience design.

#### ⏱️ Time Spent: ~90 minutes


---

### 📅 Sunday, August 3 – Highlighted Chunks + Systems Thinking

#### ✅ What I Did
- Extended `/rag-with-highlights` to return `highlighted_chunks`
- Added schema models for `Highlight`, `HighlightedChunk`, and `RAGWithHighlightsResponse`
- Tested via Swagger with term match visualization support
- Completed systems thinking reflection (Q&A)
- Integrated insights from “Thinking in Systems” into my AI design lens

#### 🧠 What I Learned

| Practice                   | What It Trains Me For                                         |
|----------------------------|---------------------------------------------------------------|
| Span-level traceability    | Improves transparency, enables debug tooling & UI overlays    |
| Schema modularity          | Builds structured response layering in real-world APIs        |
| Systems thinking (Q&A)     | Reinforces mental models for stability, leverage, and design  |
| UI-ready response shaping  | Sets foundation for explainable GenAI in enterprise apps      |

#### 🔭 Reflection
- I now see how “highlighting” chunks is more than a UI feature — it’s an **audit trail**.
- The idea of feedback loops from systems thinking maps well to logging → annotation → retriever improvement.
- I feel more confident designing APIs not just for myself, but for downstream users and reviewers.

#### 📚 Book Progress
- *Thinking in Systems* by Donella Meadows
- ✅ 104/229 pages completed

#### ⏱ Time Spent: ~90 mins

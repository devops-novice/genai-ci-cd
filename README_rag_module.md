# 🔍 Retrieval-Augmented Generation (RAG) API with CLI + Evaluation Logging

A modular, production-ready FastAPI + CLI project for building and evaluating Retrieval-Augmented Generation (RAG) systems using LangChain and OpenAI.

---

## 🚀 Features

- ✅ Modular `RAGEngine` class
- 🔌 FastAPI endpoints (`/rag-real`, `/rag-with-sources`, etc.)
- 🧠 Source-level highlighting support
- 🧪 CLI tool (`rag_cli.py`) for fast developer usage
- 📜 Structured evaluation log (`rag_eval_log.jsonl`)
- 🛠 Manual annotation tool (`eval_annotator.py`)
- 📦 Uses FAISS vector store and OpenAI LLMs (can be swapped)

---

## 🧱 Project Structure

genai-ci-cd/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI routes
│ ├── rag_engine.py # Modular RAG pipeline
│ ├── schemas.py # Input/output validation
│ ├── embedding_utils.py # Ingestion + indexing
│ └── log_utils.py # JSONL logging
├── scripts/
│ ├── embed_and_store.py # Indexing script
│ └── eval_annotator.py # Interactive evaluator
├── tests/
│ └── test_rag_engine.py # Unit test
├── docs/
│ └── AI_Leadership_Reading_Plan_Refined.md
├── logs/
│ └── rag_eval_log.jsonl # Annotated query traces
├── rag_cli.py # CLI interface for queries
├── README.md # 

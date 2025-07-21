---

## 📅 July 21, 2025 — Week 3, Day 1

### ✅ What I Did Today

- Learned about chunking strategies, metadata tagging, and multi-file RAG pipelines
- Updated the FAISS indexing script to:
  - Load all `.md` files from `docs/`
  - Chunk each with `RecursiveCharacterTextSplitter`
  - Add metadata per chunk (`source: filename`)
- Rebuilt the FAISS index with multiple files
- Successfully tested `/rag-real` to return LLM answers grounded in retrieved content
- Refactored the embedding logic into reusable functions (`embedding_utils.py`)

---

### 🧠 What I Learned

- How chunk size and overlap affect retrieval quality
- Why metadata is essential for multi-doc RAG (for filtering, debugging, future UI display)
- How to scale indexing workflows using modular scripts
- How LangChain uses vector-based search and document metadata internally

---

### 🧱 Architecture Decisions

- Kept `embed_and_store.py` lightweight — now just a runner
- Moved reusable logic into `app/embedding_utils.py` for future API use
- Retained `.md` as base input format — extensible to `.txt`, `.py`, `.pdf`

---

### 🚀 What I’d Do Next

- Add support for other file types (e.g., `.txt`, `.py`)
- Show `source` metadata in `/rag-real` response (e.g., to cite the file)
- Support real-time upload-and-embed endpoints
- Implement retrieval filtering (e.g., only from a specific file or section)

---

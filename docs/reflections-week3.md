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

---

## 📅 July 22, 2025 — Week 3, Day 2

### ✅ What I Did Today

- Learned about **failure modes in Retrieval-Augmented Generation (RAG)**:
  - Irrelevant retrieval
  - Hallucination despite context
  - Chunking boundary issues
  - Context-question mismatch
  - Embedding vocabulary drift
- Implemented three new FastAPI endpoints:
  - `/rag-real`: Returns LLM answer from semantically retrieved context
  - `/rag-with-sources`: Adds traceability by returning source files for retrieved chunks
  - `/rag-debug`: Internal-only API to inspect chunks and sources *before* generation

---

### 🧠 What I Learned

- How RAG systems can fail silently and how to **observe failure modes** through retrieval logs and metadata
- Importance of **traceability** in GenAI systems (especially for enterprise or regulated environments)
- How to version, evolve, and differentiate APIs cleanly as part of a **maturing AI product**
- Separation of concerns: retrieval vs generation vs observability
- Why chunk metadata (`source`) becomes essential in scaling RAG pipelines

---

### 🔁 Design Decisions I Made

- Preserved `/rag-real` for baseline testing
- Created new `/rag-with-sources` endpoint instead of modifying existing — supports long-term learning trace
- Introduced `/rag-debug` to inspect chunk-level retrieval independently of LLM responses
- Used `set()` to deduplicate sources and `[:300]` truncation to keep payload readable

---

### 🚀 What I’d Do Next

- Add top-k tuning and filters to `/rag-debug` (e.g., file name filter, chunk score)
- Display retrieved chunk sources alongside answers in a UI layer
- Log internal `retrieval -> generation` trace for audit/debug purposes
- Investigate use of Hybrid Retrieval (vector + keyword) for better precision

---

---

## 📅 July 23, 2025 — Week 3, Day 3

### ✅ What I Did Today

- Understood the difference between:
  - `VectorStore` (low-level index, FAISS) and
  - `Retriever` (high-level interface over vector search)
- Created a `get_retriever()` utility in `embedding_utils.py`
  - Loads FAISS index
  - Wraps it in a retriever with customizable `k`
- Added a new endpoint: `/rag-via-retriever`
  - Uses retriever abstraction instead of raw FAISS
  - Produces LLM answers + source traceability
- Verified all retrieval, generation, and modularity behavior end-to-end

---

### 🧠 What I Learned

- How **abstractions improve maintainability**
- How retrievers let you **swap vector stores** without touching endpoint code
- Why decoupling is essential for:
  - Cleaner code
  - Pluggable architectures (e.g. Pinecone, Chroma, hybrid retrievers)
  - Easier unit testing (mock retrievers)
- That even simple refactors like `get_retriever()` can unlock major flexibility

---

### 🔁 Design Thinking I Practiced

- Inverted dependency from endpoint → utility function
- Wrapped infra (FAISS) behind interface (Retriever)
- Designed for reuse and future evolution (e.g., filtering, multi-index RAG)

---

### 🚀 What I’d Like to Explore Next

- Add metadata-based filtering to retriever
- Plug in a second retriever (e.g. keyword or BM25)
- Create a hybrid or reranked retrieval pipeline
- Move retrieval config to a YAML or environment file

---


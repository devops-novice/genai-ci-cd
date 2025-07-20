# 🗂️ AI Engineering Journey — Task Log

This file tracks all major tasks and milestones in the GenAI CI/CD project.  
Each entry represents the goals, concepts learned, and outcomes delivered during the corresponding week.

---

## 📅 Week 1 – Foundations & Prompt Engineering

### ✅ Core Tasks
- Set up project repo structure (`app/`, `scripts/`, `docs/`, etc.)
- Created `.gitignore` and cleaned up logs, cache, and system files
- Set up FastAPI with logging and tested `/ask` endpoint
- Built `/structured` endpoint using `ChatPromptTemplate` + `PydanticOutputParser`
- Built `/reason` endpoint using Chain-of-Thought prompting
- Created structured logs and `reflections-week1.md`

### 🧠 Concepts Learned
- Prompt engineering basics (system/user roles)
- Output parsing for structured LLM responses
- CoT (Chain of Thought) prompting for reasoning
- FastAPI design principles
- Good repo hygiene and documentation

---

## 📅 Week 2 – RAG (Retrieval-Augmented Generation)

### ✅ Core Tasks
- Learned what embeddings are and how vector similarity search works
- Understood full RAG architecture (retrieve → inject → generate)
- Built `/rag-fake` endpoint with mock document search
- Created `scripts/embed_and_store.py` to embed text and build FAISS index
- Built `/rag-real` endpoint using:
  - `OpenAIEmbeddings`
  - FAISS vector search
  - Real LLM-grounded response generation
- Refactored deprecated LangChain imports (`langchain_community`, `langchain_openai`)
- Tested FAISS contents via debug script
- Indexed a real markdown file (`docs/devops_notes.md`)
- Added usage documentation and code comments for `/rag-real`

### 🧠 Concepts Learned
- How semantic embeddings enable smarter search
- What FAISS is and how it powers retrieval
- End-to-end RAG pipeline: from file → chunks → embeddings → LLM query
- Deserialization risks with pickle (and how to safely bypass)
- Long-term repo structuring and task traceability

---

## 📅 Week 3 → Coming Soon

Will include:
- Chunking strategy improvements
- Embedding multiple files
- Building document chat agents
- Streaming or multi-turn interactions

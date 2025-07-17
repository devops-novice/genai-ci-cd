# Week 1 Reflections – AI Upskilling Journey

## 📅 Date: July 16, 2025  
_(Adjusted Day - originally July 17 content)_

---

### ✅ What I Did Today
- Reviewed and documented key LLM concepts:
  - **Context**: Importance of token limits and input history
  - **Prompt Injection**: Risks from user-manipulated input
  - **RAG**: Combining search + generation for smarter answers
- Built a second FastAPI chain using:
  - `ChatPromptTemplate` with system/user roles
  - `PydanticOutputParser` for structured LLM output
- Added new endpoint `/structured` returning `summary` + `tone` from LLM

---

### 🔍 What I Learned
- How structured output improves reliability and composability in AI apps
- Why prompt injection is a real threat to LLM-based interfaces
- How chat-based prompts (system + human roles) differ from plain templates
- The value of using modular tools like LangChain early, even without full adoption

---

### 🧠 Questions or Confusions
- How should I balance raw model creativity vs. strict output formats?
- How do more advanced RAG systems scale beyond one document?
- How would structured output work with streaming APIs or live chat UIs?

---

### 🧭 Next Steps
- Explore how to add multiple steps or chaining (e.g., summarizing + rating tone + generating advice)
- Possibly refactor into separate modules if `main.py` grows too large
- Begin building RAG-like prototype after finishing current FastAPI exercises

---

### 🧘 Meta Reflection
I’m seeing how these small building blocks (prompt, parse, serve) form the foundation of more powerful AI systems. It's easy to fall into copy-paste loops, but by zooming out and reflecting, I’m reinforcing the **why** behind the **how**.

---

---

## 📅 July 17, 2025 (shifted)

### ✅ What I Did Today
- Learned about **Chain of Thought (CoT)** prompting and how it helps LLMs reason step-by-step.
- Documented CoT in `docs/concepts.md` with examples.
- Built a new FastAPI endpoint `/reason` that:
  - Accepts a user question
  - Uses a CoT-style prompt with LangChain
  - Returns structured output with `reasoning` and `conclusion`

### 💡 What I Learned
- CoT prompts dramatically improve logical reasoning in LLMs
- LangChain + PydanticOutputParser make it easy to extract multiple parts of an LLM response
- How to design explainable AI features via FastAPI

### 🤔 Confusions or Follow-Ups
- What are the best practices when CoT outputs become too verbose or uncertain?
- Can CoT chains be combined with RAG patterns?

### 🧭 Next Steps
- Try adding multi-step CoT + follow-up generator (like: “What should I do next based on this?”)
- Begin designing a mini RAG prototype in a few days

---

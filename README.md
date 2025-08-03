
# 🤖 GenAI for CI/CD: Prompt Engineering Playground

This repository contains hands-on experiments that apply **Generative AI** to **DevOps, CI/CD, and DevSecOps workflows** using the OpenAI API. It's part of a larger AI upskilling journey focused on becoming an AI-integrated Engineering Leader.

---

## 📂 Folder Structure

```
genai-ci-cd/
├── notebooks/        # Jupyter notebooks with hands-on GenAI tasks
│   └── genai_ci_cd_tasks.ipynb
├── scripts/          # (Optional) Python scripts version of tasks
├── docs/             # Markdown notes or writeups
└── README.md         # This file
```


---

## 🚀 Tasks Included

### ✅ Task 1: Release Note Summarization *(Notebook)*
Use GPT to convert raw git logs or changelogs into concise 3-line release notes for product managers.

### ✅ Task 2: Legacy Script Explanation *(Notebook)*
Use GPT to translate a legacy shell script into plain English for documentation or handover.

### ✅ Task 3: Risk Detection from Change Requests *(Notebook)*
Use GPT to detect missing rollback plans, testing gaps, and PROD deployment risks in change tickets.

### ✅ Task 4: FastAPI Backend with LLM Chains *(Code)*
Build real-world backend endpoints powered by structured LangChain-like logic:
- `/ask`: Simple prompt template with string output
- `/structured`: Chat prompt with structured JSON output (`summary`, `tone`)
- `/reason`: Chain of Thought reasoning endpoint with step-by-step logic (`reasoning`, `conclusion`)

---

## 🛠️ How to Run Locally

### 1. Clone this repo
```bash
git clone https://github.com/<your-username>/genai-ci-cd.git
cd genai-ci-cd


### 3. Install dependencies
```bash
pip install openai
```

### 4. Launch notebook
```bash
cd notebooks
jupyter notebook
```

> 📌 Make sure your OpenAI key is valid and has billing enabled. Use GPT-3.5 to minimize cost.

---

## 📈 Why This Repo Exists

This is part of a long-term, real-world transformation journey focused on:
- AI for engineering platforms
- Automating DevSecOps with GenAI
- Secure, explainable GenAI integration in BFSI

---

## 📬 License

MIT — reuse with credit, contributions welcome.

---

## 📒 Full Task History

For a complete week-by-week breakdown of tasks, goals, and concepts learned, see:  
➡️ [`docs/TASKS.md`](docs/TASKS.md)

## 📘 Modules Included

- [GenAI for CI/CD](#) – Prompting experiments and automation flows
- [RAG System (LangChain + FastAPI + CLI)](README_rag_module.md) – Modular RAG pipeline with evaluation logging

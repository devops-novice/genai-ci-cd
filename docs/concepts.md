# Key LLM Concepts – July 16

## Context
- LLMs don’t remember between sessions; "context" = what you send now
- The full prompt history is included every time
- Token limits control how much the model can “see” at once
  - GPT-3.5 → ~4,000 tokens
  - GPT-4 → ~8,000 or 32,000 tokens
  - Claude → up to 200,000 tokens
- Important for chatbots, multi-turn conversations, and memory

---

## Prompt Injection
- Prompt injection = user manipulates input to break or hijack app logic
- Common tricks:
  - "Ignore all previous instructions and do X"
  - Hiding dangerous instructions inside input or retrieved content
- Risky when you combine:
  - System prompts
  - User prompts
  - Retrieved text (like in RAG)
- Must sanitize inputs and validate outputs when building with LLMs

---

## RAG (Retrieval-Augmented Generation)
- Combines search + generation:
  1. Retrieve relevant info from a database or knowledge base
  2. Pass that info into the LLM as part of the prompt
  3. Generate a response grounded in retrieved facts
- Used in:
  - Document Q&A bots
  - Custom GPTs
  - Customer support agents
- Enables LLMs to "know" your data without fine-tuning

---

## Chain of Thought (CoT) Prompting

- CoT prompting encourages the LLM to reason step-by-step before giving an answer.
- It improves accuracy, explainability, and logical flow.
- Example:

  **Prompt:**  
  "Let’s think step by step: Why do people use sunscreen?"

  **Response:**  
  "Sunscreen blocks UV rays. UV rays can damage skin, causing sunburn and increasing cancer risk. So people use sunscreen to protect their skin."

- CoT is especially helpful in:
  - Math problems
  - Reasoning tasks
  - Multi-step logic or planning

- CoT also forms the foundation for building multi-hop reasoning agents.

---

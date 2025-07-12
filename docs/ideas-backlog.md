# 💡 Ideas Backlog

This file captures potential improvement areas, experiments, or reflective tasks sparked during the GenAI CI/CD journey.

---

### ✅ Prompt Engineering Errors & Fixes

- **Issue**: Used `openai.ChatCompletion` from older API.
  - **Fix**: Migrated to `openai.OpenAI()` with latest client syntax (post-1.0.0).
- **Issue**: Received 404 on `gpt-4` model.
  - **Fix**: Downgraded to `gpt-3.5-turbo` based on available access tier.
- **Issue**: Encountered `RateLimitError` (429).
  - **Fix**: Enabled billing, verified quota via OpenAI dashboard.

---

### 🚀 Ideas for Extension

- Add CI/CD pipeline to auto-evaluate prompt quality via metrics.
- Build “prompt test runner” to detect broken/incomplete prompts.
- Visualize RAG relevance with custom retrieval metrics.

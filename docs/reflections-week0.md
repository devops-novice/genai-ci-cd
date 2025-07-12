# Reflections – Week 0 (July 12–13, 2025)

## 🔍 What I Learned
- Prompt Engineering is about structure, context, and clarity—not just creativity.
- OpenAI SDK now uses `OpenAI()` clients and `chat.completions.create()` calls.
- GitHub commit automation, repo hygiene, and CLI-based versioning are essential to credibility.
- LangChain requires Python 3.8+ and compatible pip versions; PyPI updates can block older installs.
- Every commit counts — even small documentation, test, or clean-up updates improve visibility.

---

## 🤯 What Surprised Me

- SDK version mismatches can break working code:
  - ❌ `openai.ChatCompletion.create()` → deprecated in `openai>=1.0.0`
  - ✅ Fixed by switching to `client.chat.completions.create()` via `OpenAI()` object.

- Quota and model access errors are easy to miss:
  - ❌ Error: `'gpt-4' model not available`
  - ✅ Resolution: Downgraded to `gpt-3.5-turbo` for now until paid access is confirmed.

- Authentication failures in `git push`:
  - ❌ Password-based login deprecated by GitHub.
  - ✅ Resolution: Used **GitHub personal access token (PAT)** and stored via `git-credential`.

- Git commit failed due to missing identity:
  - ❌ `Author identity unknown`
  - ✅ Resolution: Ran `git config --global user.name` and `user.email` to set identity.

- Pip install errors for `langchain`:
  - ❌ `Could not find a version that satisfies the requirement langchain`
  - ✅ Resolution: Verified Python version (3.10), ensured `pip` was upgraded.

---

## 🧠 Errors Faced & Fixes (as quick cheatsheet)

| Error | Root Cause | Fix |
|-------|------------|-----|
| `APIRemovedInV1` | Old syntax from OpenAI SDK v0.28 | Migrate to v1.0 syntax using `client.chat.completions.create()` |
| `The model 'gpt-4' does not exist` | No GPT-4 access under current API plan | Downgrade to `gpt-3.5-turbo` |
| `openai.OpenAIError: api_key must be set` | Env variable not loaded | Use `.env` file or pass `api_key` in `OpenAI()` |
| `RateLimitError / quota exceeded` | Free tier quota exhausted | Activate paid billing in OpenAI account |
| `Could not find a version for langchain` | Incompatible pip or Python | Upgrade pip: `pip install --upgrade pip` |
| `git push rejected (fetch first)` | Remote repo changed since last pull | Run `git pull --rebase` before push |
| `Author identity unknown` | Git config missing username/email | Run `git config --global user.name/email` |
| `password authentication failed` | GitHub removed password-based login | Use PAT and cache via `git config credential.helper` |

---

## 🤖 Practical Ideas Sparked (based on AI industry trends)

| Idea | Why It Matters | Next Step |
|------|----------------|-----------|
| Prompt-Powered SRE Runbook Assistant | Reduces MTTR, aligns with DORA | Turn resolution patterns into prompt chains |
| Change Risk Evaluator | Adopted by JPMorgan, GitHub Labs | Prompt tune CR descriptions for risk scores |
| Git Commit Classifier Bot | Used in Copilot PR Suggestions | Use LangChain + GitHub API to test classification |
| Postmortem Generator | incident.io uses it in production | Feed alerts + slack → generate summary |
| GenAI PR Reviewer | GitHub uses this internally | Build prompt template with “flag, suggest, rewrite” |
| CI/CD Risk Heatmap | Predict unstable areas | Feed LangChain output into FastAPI + Grafana |
| GenAI Usage Auditor | Needed for compliance | Extract token logs and cost patterns |
| Inner Loop Prompt Tester | Encourages fast yet safe prompting | Bundle prompt+test+feedback into CLI tool |

---

## 📘 What I Want to Improve

- Think in **reusable prompt patterns**, not just one-off chains
- Add **token usage tracking and visualization**
- Explore **prompt testing** via Guardrails, Rebuff, Trulens
- Learn **vector DB tuning**: chunking, metadata filters, embedding selection
- Integrate GenAI pipelines with **GitHub Actions and CI triggers**
- Understand implications of **AI compliance and audit-readiness**

---

## 🧠 Mindset Shift

> I am not just building AI scripts — I am shaping reusable engineering logic for GenAI-augmented platforms.

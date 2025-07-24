# scripts/test_retriever.py

from app.embedding_utils import get_retriever

retriever = get_retriever(filters={"source": "AI_Leadership_Reading_Plan_Refined.md"})
results = retriever.invoke("What is CI/CD?")  # ✅ Modern usage

for i, doc in enumerate(results):
    print(f"[{i+1}] Source: {doc.metadata.get('source')}\n{doc.page_content[:200]}\n")


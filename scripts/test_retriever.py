# scripts/test_retriever.py

from app.embedding_utils import get_retriever

retriever = get_retriever()
results = retriever.get_relevant_documents("What is CI/CD?")
for i, doc in enumerate(results):
    print(f"[{i+1}] Source: {doc.metadata.get('source')}\n{doc.page_content[:200]}\n")

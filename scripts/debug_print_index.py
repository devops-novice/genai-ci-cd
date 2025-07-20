# scripts/debug_print_index.py

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

docs = vectorstore.similarity_search("Print all", k=10)

for i, doc in enumerate(docs):
    print(f"Doc {i+1}: {doc.page_content}")


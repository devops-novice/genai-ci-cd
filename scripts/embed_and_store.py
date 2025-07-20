# scripts/embed_and_store.py

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

# Set your OpenAI key
#os.environ["OPENAI_API_KEY"] = "sk-..."  # Or load from .env

# Sample document (you can load from file too)
docs = [
    "CI/CD automates the process of software delivery and infrastructure changes.",
    "Docker is a platform used to containerize applications.",
    "Monitoring helps detect issues in production systems.",
    "Git is a distributed version control system used in modern DevOps workflows."
]

# Step 1: Chunk the documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
documents = text_splitter.create_documents(docs)

# Step 2: Generate embeddings
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embedding_model)

# Step 3: Save FAISS index locally
vectorstore.save_local("faiss_index")
print("✅ FAISS index created and saved to ./faiss_index")

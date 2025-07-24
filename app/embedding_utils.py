# app/embedding_utils.py

import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def load_and_split_markdown_files(docs_dir: str = "docs", chunk_size=300, overlap=50):
    docs_path = Path(docs_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    all_chunks = []

    for file in docs_path.glob("*.md"):
        loader = TextLoader(str(file))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file.name
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)

    return all_chunks

def create_and_save_faiss_index(chunks, index_dir="faiss_index"):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_dir)
    print(f"✅ Saved FAISS index with {len(chunks)} chunks → {index_dir}")


# app/embedding_utils.py

from typing import Optional, Dict
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def get_retriever(index_path: str = "faiss_index", k: int = 3, filters: Optional[Dict] = None):

    """
    Load a retriever backed by FAISS.
    
    Parameters:
    - index_path: path to saved FAISS index
    - k: number of documents to retrieve
    - filters: optional metadata filter dict (e.g., {"source": "devops_notes.md"})
    
    Returns:
    - Retriever object supporting get_relevant_documents()
    """

    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)

    search_kwargs = {"k": k}
    if filters:
        search_kwargs["filter"] = filters

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    return retriever


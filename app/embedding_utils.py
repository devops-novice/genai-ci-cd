# app/embedding_utils.py

import os
from pathlib import Path
from typing import Optional, Dict
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings

# ---- Stable chunk IDs --------------------------------------------------------
def make_chunk_id(filename: str, chunk_index: int) -> str:
    """
    Build deterministic IDs that both the retriever and golden set can use.
    Example: "reflections-week1.md#chunk12"
    """
    return f"{filename}#chunk{chunk_index}"
# -----------------------------------------------------------------------------


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

# >>> NEW: add deterministic IDs per chunk (per-file numbering) <<<
        for i, c in enumerate(chunks):
            c.metadata["chunk_id"] = make_chunk_id(file.name, i)  # e.g. policy.md#chunk0
            c.metadata["id"] = c.metadata["chunk_id"]             # alias used by retriever / golden set

        all_chunks.extend(chunks)

    return all_chunks

def create_and_save_faiss_index(chunks, index_dir="faiss_index"):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_dir)
    print(f"✅ Saved FAISS index with {len(chunks)} chunks → {index_dir}")


# app/embedding_utils.py
def get_retriever(index_path: str = "faiss_index", k: int = 3, filters: Optional[Dict] = None):
    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)

    search_kwargs = {"k": k}
    if filters:
        search_kwargs["filter"] = filters

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    return retriever


def get_embedder():
    # Supported by fastembed across versions; lightweight & good quality
    return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")


def create_and_save_faiss_index(documents, dest_dir: str = "faiss_index"):
    emb = get_embedder()
    try:
        dim = len(emb.embed_query("probe"))
        print(f"[ingest] using embedder dim={dim}")
    except Exception:
        pass
    vs = FAISS.from_documents(documents, emb)
    vs.save_local(dest_dir)

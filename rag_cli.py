# rag_cli.py

import argparse
from app.rag_engine import RAGEngine

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from app.embedding_utils import get_retriever


def main():
    parser = argparse.ArgumentParser(description="Query your RAG system via CLI")
    parser.add_argument('--query', type=str, required=True, help="The question to ask")
    parser.add_argument('--source', type=str, help="Optional: Restrict to a specific source file")

    args = parser.parse_args()
    engine = RAGEngine(source_filter=args.source)

    result = engine.query(args.query)

    print("\n🧠 Answer:\n", result.answer)
    print("\n📄 Sources:")
    for s in result.sources:
        print(" -", s)

    print("\n📚 Chunks Used (truncated):")
    for i, c in enumerate(result.chunks):
        print(f"\n--- Chunk {i+1} ---\n{c[:300]}...")  # show only first 300 chars

if __name__ == "__main__":
    main()

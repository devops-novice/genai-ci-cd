import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.rag_engine import RAGEngine

def test_basic_query():
    engine = RAGEngine()
    result = engine.query("What is SimpleDirectoryReader?")
    assert "SimpleDirectoryReader" in result["answer"]
    assert len(result["chunks"]) > 0

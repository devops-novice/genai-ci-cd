from app.embedding_utils import get_retriever

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from app.embedding_utils import get_retriever

# app/rag_engine.py
from app.retrieval import retrieve_topk     # NEW
from app.generator import generate_answer   # NEW

class RAGEngine:
    def __init__(self, index_path="faiss_index", k=3, source_filter=None):
        self.k = k
        self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        self.prompt_template = PromptTemplate.from_template("""
        You are an assistant helping answer questions based on internal DevOps knowledge.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """)
        if source_filter:
            self.retriever = get_retriever(filters={"source": source_filter})
        else:
            from langchain_community.vectorstores import FAISS
            from langchain_openai import OpenAIEmbeddings
            self.vectorstore = FAISS.load_local(index_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    def query(self, question: str):
        docs = self.retriever.get_relevant_documents(question) if hasattr(self, 'retriever') else self.vectorstore.similarity_search(question, k=self.k)
        context = "\n---\n".join(doc.page_content for doc in docs)
        prompt = self.prompt_template.format(context=context, question=question)
        result = self.llm.invoke(prompt)
        sources = list({doc.metadata.get("source", "unknown") for doc in docs})

        from pydantic import BaseModel

        class RAGResponse(BaseModel):
            answer: str
            sources: list[str]
            chunks: list[str]

        return RAGResponse(answer=result.content, sources=sources, chunks=[doc.page_content for doc in docs])

# inside app/rag_engine.py
from .eval_metrics import precision_at_k, recall_at_k, hit_at_k, mrr, exact_match, f1_tokens
from .faithfulness import check_faithfulness

def evaluate_rag(question: str, gold_answer: str, expected_source_ids: list[str], k: int = 5, run_config: dict | None = None):
    run_config = run_config or {}
    # Use your existing retrieval/generation utilities
    retrieved = retrieve_topk(question, k=k, cfg=run_config.get("retriever", {}))  # returns [{"id":..., "text":...}, ...]
    answer, used_ids = generate_answer(question, retrieved, cfg=run_config.get("generator", {}))
    r_ids = [r["id"] for r in retrieved]

    retrieval = {
        "k": k,
        "hit_at_k": hit_at_k(r_ids, expected_source_ids, k),
        "precision_at_k": precision_at_k(r_ids, expected_source_ids, k),
        "recall_at_k": recall_at_k(r_ids, expected_source_ids, k),
        "mrr": mrr(r_ids, expected_source_ids),
        "retrieved_ids": r_ids,
    }
    generation = {
        "exact_match": exact_match(answer, gold_answer),
        "f1": f1_tokens(answer, gold_answer),
    }
    faith = check_faithfulness(answer, retrieved, expected_source_ids)

    return {"retrieval": retrieval, "generation": generation, "faithfulness": faith, "answer": answer}

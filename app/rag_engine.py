from app.embedding_utils import get_retriever

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from app.embedding_utils import get_retriever

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

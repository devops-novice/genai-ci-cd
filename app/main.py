import os
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from app.embedding_utils import get_retriever
from app.schemas import PromptRequest
from app.schemas import RAGResponse

from .eval_router import router as eval_router
from .rag_router import router as rag_router   # NEW

#Build the CoT Chain
from app.schemas import ReasoningOutput
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Modularize RAG into a RAGEngine class
from app.rag_engine import RAGEngine
engine = RAGEngine()


# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Initialize logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)



app = FastAPI()
app.include_router(eval_router)
app.include_router(rag_router)                 # NEW

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = PromptTemplate.from_template("You are a DevOps expert. Help answer this question: {question}")

chain = prompt | llm | StrOutputParser()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_genai(query: Query):
    logger.info(f"Received question: {query.question}")
    result = chain.invoke({"question": query.question})
    logger.info(f"Generated response: {result}")
    return {"response": result}


from app.schemas import Analysis
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser

#class PromptRequest(BaseModel):
#    prompt: str

parser = PydanticOutputParser(pydantic_object=Analysis)

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant that analyzes user input."),
    HumanMessagePromptTemplate.from_template("Analyze the following text:\n{input}\n\n{format_instructions}")
])

@app.post("/structured", response_model=Analysis)
async def analyze_prompt(data: PromptRequest):
    messages = chat_prompt.format_messages(
        input=data.prompt,
        format_instructions=parser.get_format_instructions()
    )
    result = llm(messages)
    parsed = parser.parse(result.content)
    return parsed


cot_parser = PydanticOutputParser(pydantic_object=ReasoningOutput)

cot_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a thoughtful assistant who explains reasoning step by step."),
    HumanMessagePromptTemplate.from_template("Question: {question}\n\n{format_instructions}")
])
@app.post("/reason", response_model=ReasoningOutput)
async def get_reasoning(data: PromptRequest):
    messages = cot_prompt.format_messages(
        question=data.prompt,
        format_instructions=cot_parser.get_format_instructions()
    )
    result = llm(messages)
    parsed = cot_parser.parse(result.content)
    return parsed

#July 18, 2025 Tasks
#Step 1: Prepare Simulated Docs
fake_documents = [
    {"id": 1, "content": "Docker is a tool for packaging applications using containers."},
    {"id": 2, "content": "CI/CD automates building, testing, and deploying code."},
    {"id": 3, "content": "Monitoring tools help detect downtime and alert engineers."},
    {"id": 4, "content": "Git is a distributed version control system."}
]

# Step 2: Write a Simple “Retriever” Function
def retrieve_docs(user_query: str, top_k: int = 2):
    hits = []
    for doc in fake_documents:
        if any(word.lower() in doc["content"].lower() for word in user_query.split()):
            hits.append(doc["content"])
    return hits[:top_k]

# Step 3: Create a Prompt Template
rag_prompt = PromptTemplate.from_template("""
You are an expert assistant. Use the following context to answer the question:

Context:
{context}

Question:
{question}

Answer:
""")

rag_parser = StrOutputParser()

# Step 4: Create the /rag-fake Endpoint
@app.post("/rag-fake", response_model=RAGResponse)
async def rag_fake(data: PromptRequest):
    context_docs = retrieve_docs(data.prompt)
    context_str = "\n---\n".join(context_docs)

    formatted_prompt = rag_prompt.format(
        context=context_str,
        question=data.prompt
    )
    result = llm.invoke(formatted_prompt)
    #return {"answer": rag_parser.parse(result)}
    return {"answer": result.content}

# July 20, 2025 
# app/main.py (append below your other endpoints)

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load the FAISS index
vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

# Set up LLM and prompt
llm_rag = ChatOpenAI(model="gpt-3.5-turbo")

rag_prompt_template = PromptTemplate.from_template("""
You are an assistant helping answer questions based on internal DevOps knowledge.

Context:
{context}

Question:
{question}

Answer:
""")

@app.post("/rag-real", response_model=RAGResponse)
async def rag_real(data: PromptRequest):
    # Step 1: Embed and search top 3 similar chunks
    docs = vectorstore.similarity_search(data.prompt, k=3)
    context = "\n---\n".join(doc.page_content for doc in docs)

    # Step 2: Inject into prompt
    formatted_prompt = rag_prompt_template.format(
        context=context,
        question=data.prompt
    )

    # Step 3: Generate answer
    result = llm_rag.invoke(formatted_prompt)

    return {"answer": result.content}

"""
POST /rag-with-sources
Enhanced RAG endpoint that:
- Performs FAISS-based semantic retrieval
- Injects context into LLM prompt
- Returns grounded answer and list of source file(s) retrieved
"""
@app.post("/rag-with-sources", response_model=RAGResponse)
async def rag_with_sources(data: PromptRequest):
    docs = vectorstore.similarity_search(data.prompt, k=3)

    # Extract content + track unique sources
    context = "\n---\n".join(doc.page_content for doc in docs)
    sources = list({doc.metadata.get("source", "unknown") for doc in docs})

    # Build prompt
    formatted_prompt = rag_prompt_template.format(
        context=context,
        question=data.prompt
    )

    result = llm_rag.invoke(formatted_prompt)
     
# --- Log the query-response ---
    from app.log_utils import log_rag_eval  # adjust import if in same file
    log_rag_eval({
        "query": data.prompt,
        "answer": result.content,
        "sources": sources,
        "chunks": [doc.page_content for doc in docs]
        # Optionally: add eval fields manually later
    })

    return {
        "answer": result.content,
        "sources": sources
    }


"""
POST /rag-debug
Internal-use endpoint for inspecting retrieved documents:
- No LLM call
- Returns chunks and their metadata
"""
@app.post("/rag-debug", response_model=RAGResponse)
async def rag_debug(data: PromptRequest):
    """
    RAG internal debug endpoint:
    - Returns retrieved chunks and their source metadata
    - No LLM call — for inspection only
    """

    docs = vectorstore.similarity_search(data.prompt, k=5)

    debug_chunks = [
        {
            "source": doc.metadata.get("source", "unknown"),
            "content": doc.page_content[:300]  # Truncate for readability
        }
        for doc in docs
    ]

    return {
        "query": data.prompt,
        "retrieved_chunks": debug_chunks
    }


@app.post("/rag-via-retriever", response_model=RAGResponse)
async def rag_via_retriever(data: PromptRequest):
    """
    RAG endpoint using clean retriever abstraction.
    Uses get_relevant_documents() instead of vectorstore.similarity_search().
    """

    retriever = get_retriever()
    docs = retriever.get_relevant_documents(data.prompt)

    context = "\n---\n".join(doc.page_content for doc in docs)
    sources = list({doc.metadata.get("source", "unknown") for doc in docs})

    formatted_prompt = rag_prompt_template.format(
        context=context,
        question=data.prompt
    )

    result = llm_rag.invoke(formatted_prompt)

    return {
        "answer": result.content,
        "sources": sources
    }


@app.post("/rag-with-filter", response_model=RAGResponse)
async def rag_with_filter(data: PromptRequest):
    """
    RAG endpoint with optional metadata filter (e.g., source-level restriction).
    """

    # Define a static filter here (you can later make it dynamic via payload)
    filters = {"source": "AI_Leadership_Reading_Plan_Refined.md"}  # Replace with your real file source

    retriever = get_retriever(filters=filters)
    logger.info(f"Retriever loaded with filters: {filters}")

    docs = retriever.invoke(data.prompt)
    logger.info(f"Retrieved {len(docs)} document(s) for prompt: '{data.prompt}'")

    for i, doc in enumerate(docs):
        logger.debug(f"[Doc {i+1}] Source: {doc.metadata.get('source')} — First 100 chars: {doc.page_content[:100]}")


    context = "\n---\n".join(doc.page_content for doc in docs)
    sources = list({doc.metadata.get("source", "unknown") for doc in docs})

    formatted_prompt = rag_prompt_template.format(
        context=context,
        question=data.prompt
    )

    result = llm_rag.invoke(formatted_prompt)

    logger.debug(f"Final RAG prompt sent to LLM:\n{formatted_prompt}")
    logger.debug(f"LLM response: {result.content[:200]}...")

    return {
        "answer": result.content,
        "sources": sources,
        "applied_filter": filters
    }


@app.post("/rag-verbose", response_model=RAGResponse)
async def rag_verbose(data: PromptRequest):
    """
    Returns full RAG trace: answer, chunks, prompt, sources, and applied filter.
    Useful for debugging and internal review.
    """

    # Optional static filter — can be parameterized later
    filters = {"source": "AI_Leadership_Reading_Plan_Refined.md"}

    retriever = get_retriever(filters=filters)
    logger.info(f"[RAG-VERBOSE] Filter used: {filters}")

    docs = retriever.invoke(data.prompt)
    logger.info(f"[RAG-VERBOSE] Retrieved {len(docs)} docs for: '{data.prompt}'")

    context_chunks = []
    sources = set()

    for doc in docs:
        chunk = doc.page_content
        source = doc.metadata.get("source", "unknown")
        context_chunks.append({"source": source, "content": chunk[:300]})
        sources.add(source)

    context_str = "\n---\n".join(doc["content"] for doc in context_chunks)

    formatted_prompt = rag_prompt_template.format(
        context=context_str,
        question=data.prompt
    )

    result = llm_rag.invoke(formatted_prompt)

    logger.debug(f"[RAG-VERBOSE] Prompt:\n{formatted_prompt}")
    logger.debug(f"[RAG-VERBOSE] Answer: {result.content[:200]}...")

    return {
        "answer": result.content,
        "question": data.prompt,
        "formatted_prompt": formatted_prompt,
        "retrieved_chunks": context_chunks,
        "sources": list(sources),
        "applied_filter": filters
    }


@app.post("/rag-configurable", response_model=RAGResponse)
async def rag_configurable(data: PromptRequest):
    """
    A RAG endpoint that accepts dynamic config:
    {
      "prompt": "...",
      "config": {
        "filters": {"source": "..."},
        "k": 3
      }
    }
    """

    print(f"DEBUG: PromptRequest object: {data.__dict__}")

    # Extract config values with safe defaults
    filters = data.config.get("filters") if data.config else None
    k = data.config.get("k") if data.config and "k" in data.config else 3

    retriever = get_retriever(k=k, filters=filters)
    logger.info(f"[RAG-CONFIG] Using filters={filters}, k={k}")

    docs = retriever.invoke(data.prompt)
    context_chunks = []
    sources = set()

    for doc in docs:
        chunk = doc.page_content
        source = doc.metadata.get("source", "unknown")
        context_chunks.append({"source": source, "content": chunk[:300]})
        sources.add(source)

    context_str = "\n---\n".join(doc["content"] for doc in context_chunks)

    formatted_prompt = rag_prompt_template.format(
        context=context_str,
        question=data.prompt
    )

    result = llm_rag.invoke(formatted_prompt)

    return {
        "answer": result.content,
        "question": data.prompt,
        "applied_config": {
            "filters": filters,
            "k": k
        },
        "sources": list(sources),
        "chunks_used": context_chunks
    }

from app.schemas import RAGWithHighlightsResponse, HighlightedChunk, Highlight

@app.post("/rag-with-highlights", response_model=RAGWithHighlightsResponse)
async def rag_with_highlights(data: PromptRequest):
    docs = vectorstore.similarity_search(data.prompt, k=3)
    context = "\n---\n".join(doc.page_content for doc in docs)

    formatted_prompt = rag_prompt_template.format(context=context, question=data.prompt)
    result = llm_rag.invoke(formatted_prompt)

    query_terms = [w.lower() for w in data.prompt.split() if len(w) > 2]
    highlighted_chunks = []

    for doc in docs:
        text = doc.page_content
        highlights = []

        for word in query_terms:
            start = text.lower().find(word)
            if start != -1:
                highlights.append(Highlight(
                    term=word,
                    start_index=start,
                    end_index=start + len(word)
                ))

        highlighted_chunks.append(HighlightedChunk(
            source=doc.metadata.get("source", "unknown"),
            content=text,
            highlights=highlights
        ))

    return RAGWithHighlightsResponse(
        answer=result.content,
        highlighted_chunks=highlighted_chunks
    )


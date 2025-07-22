import os
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

#Build the CoT Chain
from app.schemas import ReasoningOutput
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Initialize logging
log_file = f"logs/genai_log_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

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

class PromptRequest(BaseModel):
    prompt: str

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
@app.post("/rag-fake")
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

@app.post("/rag-real")
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
@app.post("/rag-with-sources")
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

    return {
        "answer": result.content,
        "sources": sources
    }

import os
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

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

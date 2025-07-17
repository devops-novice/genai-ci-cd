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

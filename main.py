from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

app = FastAPI()

# Define your LangChain components
llm = OpenAI(temperature=0.5)
prompt = PromptTemplate.from_template("Answer this: {question}")
parser = StrOutputParser()

# Chain the components
chain = prompt | llm | parser

# Define input schema
class PromptInput(BaseModel):
    question: str

# Define output schema (optional)
class GenAIResponse(BaseModel):
    answer: str

# FastAPI POST endpoint
@app.post("/generate", response_model=GenAIResponse)
def generate_response(input: PromptInput):
    result = chain.invoke({"question": input.question})
    return {"answer": result}

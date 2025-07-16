# app/llm_chain.py

from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chat_models import ChatOpenAI
from app.schemas import Analysis

parser = PydanticOutputParser(pydantic_object=Analysis)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant that analyzes user input."),
    HumanMessagePromptTemplate.from_template("Analyze the following text:\n{text}\n\n{format_instructions}")
])

# app/llm_chain.py (continued)

llm = ChatOpenAI(temperature=0)

def analyze_text(user_input: str) -> Analysis:
    formatted_prompt = prompt.format_messages(
        text=user_input,
        format_instructions=parser.get_format_instructions()
    )
    output = llm(formatted_prompt)
    return parser.parse(output.content)

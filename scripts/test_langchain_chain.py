from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create a dynamic prompt
template = "What is a DevOps engineer's role in {domain}?"
prompt = PromptTemplate.from_template(template)

# Chain prompt + LLM
chain = prompt | llm

# Invoke chain
response = chain.invoke({"domain": "incident management"})

print("🧠 LangChain Response:")
print(response.content)

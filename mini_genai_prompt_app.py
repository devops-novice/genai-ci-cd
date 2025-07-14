from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Define your prompt template
prompt = PromptTemplate.from_template(
    "As an AI assistant for platform engineering, answer this: {query}"
)

# Step 2: Initialize LLM (requires your OPENAI_API_KEY to be set)
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.3)

# Step 3: Define the output parser
output_parser = StrOutputParser()

# Step 4: Build the runnable chain using the pipe operator
chain = prompt | llm | output_parser

# Step 5: Provide user input
user_query = "What are the best practices to reduce TOIL in DevSecOps pipelines?"

# Step 6: Run the chain
response = chain.invoke({"query": user_query})

# Step 7: Output the response
print("🧠 AI Response:\n", response)

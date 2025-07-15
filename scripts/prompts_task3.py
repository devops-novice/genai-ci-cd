# prompts_task3.py

import openai
import os

# Set up client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# OR use direct key: client = openai.OpenAI(api_key="sk-...")

# Change request to analyze
change_request = """
Deploying new feature toggle to enable auto-pay for 5% of users in PROD.
Feature has passed testing in UAT environment.
No explicit rollback mechanism is documented.
Monitoring will be done through existing Splunk alerts.
"""

# Prompt for risk analysis
system_prompt = "You are an SRE assistant that reviews CI/CD change requests for risk. Highlight unclear rollback plans, production impact, and testing gaps."
user_prompt = f"Analyze the following change request and identify any risks or missing details:\n{change_request}"

# API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

# Output
print("🚨 RISK ANALYSIS:\n")
print(response.choices[0].message.content)

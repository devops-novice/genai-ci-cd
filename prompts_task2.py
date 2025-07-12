# prompts_task2.py

import openai
import os

# Set up client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# OR use direct key: client = openai.OpenAI(api_key="sk-...")

# Shell script to analyze
legacy_code = """
#!/bin/bash
for file in *.log; do
  grep -i 'error' "$file" >> errors_found.txt
done
"""

# Prompt for explanation
system_prompt = "You are a senior DevOps engineer who explains legacy shell scripts in simple terms for documentation."
user_prompt = f"Explain what this legacy shell script does, step by step:\n{legacy_code}"

# API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

# Output
print("🧾 LEGACY SCRIPT EXPLANATION:\n")
print(response.choices[0].message.content)

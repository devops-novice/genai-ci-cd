# prompts_task1.py

import openai
import os

# Set your API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# OR use direct key (if env not set): client = openai.OpenAI(api_key="sk-...")

# System and user prompts
system_prompt = "You are a professional technical writer generating release notes from commit logs."
user_prompt = """
Please generate a concise 3-line release note from the following log:

- Added retry logic to payment gateway
- Refactored audit logging to reduce latency
- Fixed edge case bug in webhook validation
- Updated README and CI workflow metadata
"""

# Ask GPT
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

# Print result
print("📦 RELEASE NOTES:")
print(response.choices[0].message.content)

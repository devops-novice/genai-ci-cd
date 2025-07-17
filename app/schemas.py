# app/schemas.py

from pydantic import BaseModel

class Analysis(BaseModel):
    summary: str
    tone: str

# app/schemas.py

class ReasoningOutput(BaseModel):
    reasoning: str
    conclusion: str

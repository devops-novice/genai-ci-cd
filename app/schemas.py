# app/schemas.py

from pydantic import BaseModel

class Analysis(BaseModel):
    summary: str
    tone: str

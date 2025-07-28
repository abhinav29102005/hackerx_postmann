# hackrx_app/core/schemas.py

from typing import List
from pydantic import BaseModel, Field, HttpUrl

class HackRxRequest(BaseModel):
    documents: HttpUrl = Field(..., description="URL to the policy PDF document.")
    questions: List[str] = Field(..., min_length=1, description="List of questions to ask about the document.")

class HackRxResponse(BaseModel):
    answers: List[str] = Field(..., description="List of answers corresponding to the questions.")
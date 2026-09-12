from pydantic import BaseModel

class VerdictModel(BaseModel):
    approved: bool
    final_answer: str
    reason: str
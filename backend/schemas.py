from pydantic import BaseModel

class ScreeningResult(BaseModel):
    score: int                   # 0–100 match score
    strengths: list[str]         # what the candidate does well
    gaps: list[str]              # what's missing
    summary: str                 # 1-2 sentence verdict
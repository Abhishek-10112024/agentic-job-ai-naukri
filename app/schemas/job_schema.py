from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    location: str
    description: str
    link: str
    source: str
    score: float = 0
    reason: str = ""
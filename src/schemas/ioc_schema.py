# IOC Schema
from pydantic import BaseModel
from typing import List


class IOCAnalysis(BaseModel):
    title: str
    summary: str
    possible_threat: str
    severity: str
    recommendations: List[str]
    evidence: List[str]
    confidence: float
# Schemas
from __future__ import annotations

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


SeverityLevel = Literal["low", "medium", "high", "critical"]
RouteType = Literal[
    "rag",
    "ioc",
    "vulnerability",
    "detection",
    "general",
    "report",
]


class ToolEvidence(BaseModel):
    """
    Standard evidence object returned by tools.

    Every specialist tool should try to return information in this shape
    so the final composer can merge results consistently.
    """

    tool_name: str = Field(..., description="Name of the tool or integration")
    status: Literal["ok", "partial", "error"] = "ok"
    summary: str = ""
    data: dict[str, Any] = Field(default_factory=dict)
    raw_text: Optional[str] = None
    source_refs: list[str] = Field(default_factory=list)


class CybersecurityAnswer(BaseModel):
    """
    Final normalized answer shown to the user.

    The Streamlit UI will render this object into cards, sections, or chat bubbles.
    """

    title: str = "Cybersecurity Analysis"
    summary: str = ""
    possible_threat: str = ""
    severity: SeverityLevel = "low"
    recommendations: list[str] = Field(default_factory=list)
    iocs: list[str] = Field(default_factory=list)
    mitre_techniques: list[str] = Field(default_factory=list)
    evidence: list[ToolEvidence] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    notes: list[str] = Field(default_factory=list)
from __future__ import annotations

from src.graph.subgraphs.threat_intel_subgraph import (build_threat_intel_subgraph)

from typing import Any

from langgraph.graph import END, START, StateGraph

from src.core.schemas import CybersecurityAnswer
from src.core.state import AppState
from src.graph.router import classify_route

from src.graph.subgraphs.detection_subgraph import build_detection_subgraph

def build_supervisor_graph(rag_graph):
    """
    Build the top-level supervisor graph.

    For now the supervisor knows how to:
    - route document/policy-like requests to the RAG subgraph
    - return a simple fallback for everything else

    This is the right place to add more specialist subgraphs later:
    - IOC enrichment
    - vulnerability triage
    - detection engineering
    - reporting
    """
    def route_node(state: AppState) -> dict[str, Any]:
        user_text = state.get("user_text", "")
        uploaded_text = state.get("uploaded_text", "")
        active_route = classify_route(
            user_text=user_text,
            uploaded_text=uploaded_text,
            knowledge_base_ready=bool(state.get("retrieved_docs")),
        )
        return {"active_route": active_route}

    def choose_next(state: AppState) -> str:
        route = state.get("active_route", "general")
        return route

    def fallback_node(state: AppState) -> dict[str, Any]:
        answer = CybersecurityAnswer(
            title="Cybersecurity Assistant",
            summary=(
                "This request does not match the current specialist path yet. "
                "Right now the system is focused on document-aware cybersecurity "
                "analysis through the RAG subgraph."
            ),
            possible_threat="Not analyzed yet",
            severity="low",
            recommendations=[
                "Try a document, pasted security text, log snippet, or policy question.",
                "More specialist tools will be added in the next phases.",
            ],
            confidence=0.25,
        )
        return {"final_answer": answer.model_dump()}

    builder = StateGraph(AppState)

    threat_graph = build_threat_intel_subgraph()
    detection_graph = build_detection_subgraph()

    builder.add_node("route", route_node)
    builder.add_node("rag", rag_graph)
    builder.add_node("threat_intel",threat_graph)
    builder.add_node("detection", detection_graph)
    builder.add_node("fallback", fallback_node)

    builder.add_edge(START, "route")
    builder.add_conditional_edges(
    "route",
    choose_next,
    {
        "rag": "rag",
        "threat_intel": "threat_intel",
        "general": "fallback",
        "detection": "detection",
        "report": "fallback",
    },
)
    builder.add_edge("rag", END)
    builder.add_edge("threat_intel",END)
    builder.add_edge("detection", END)
    builder.add_edge("fallback", END)

    return builder.compile()
# State
from __future__ import annotations

from typing import Any, TypedDict
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage


class AppState(TypedDict, total=False):
    """
    Shared graph state.

    This is the data that flows through the supervisor and all specialist subgraphs.
    Keep it small, structured, and easy to inspect.
    """

    # Chat history
    messages: Annotated[list[BaseMessage], add_messages]

    # User input
    user_text: str
    uploaded_text: str
    active_route: str

    # Raw extracted entities
    extracted_iocs: dict[str, Any]

    extracted_ips: list[str]
    extracted_urls: list[str]
    extracted_domains: list[str]
    extracted_hashes: list[str]
    extracted_emails: list[str]
    extracted_cves: list[str]

    # Tool outputs
    retrieved_docs: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]

    # # Threat intelligence outputs
    # vt_results: list[dict[str, Any]]
    # nvd_results: list[dict[str, Any]]

    # # Merged evidence
    # evidence: list[dict[str, Any]]

    # Threat Intelligence
    vt_results: list[dict[str, Any]]
    nvd_results: list[dict[str, Any]]
    misp_results: list[dict[str, Any]]
    
    evidence: list[dict[str, Any]]

    # Detection outputs
    mitre_techniques: list[dict[str, Any]]
    sigma_rule: str
    yara_rule: str

    # Final response
    final_answer: str

    # Metadata
    thread_id: str
    session_id: str
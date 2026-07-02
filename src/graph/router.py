from __future__ import annotations

import re

from src.core.schemas import RouteType


CVE_PATTERN = re.compile(r"\bcve-\d{4}-\d{4,7}\b", re.IGNORECASE)
IP_PATTERN = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
URL_PATTERN = re.compile(r"(?:https?|hxxp)://[^\s]+", re.IGNORECASE)
HASH_PATTERN = re.compile(r"\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b", re.IGNORECASE)

IOC_HINTS = (
    "ip address",
    "domain",
    "url",
    "hash",
    "ioc",
    "indicator of compromise",
    "virus total",
    "virustotal",
    "abuseipdb",
    "urlscan",
)
VULN_HINTS = (
    "vulnerability",
    "exploit",
    "patch",
    "cve",
    "cvss",
    "zero-day",
    "kev",
)
DETECTION_HINTS = (
    "mitre",
    "attack",
    "sigma",
    "yara",
    "powershell",
    "brute force",
    "failed login",
    "log",
    "event",
    "siem",
)
RAG_HINTS = (
    "policy",
    "playbook",
    "handbook",
    "procedure",
    "document",
    "pdf",
    "report",
    "sop",
    "guide",
)


# def classify_route(
#     user_text: str,
#     uploaded_text: str = "",
#     knowledge_base_ready: bool = False,
# ) -> RouteType:
#     """
#     Decide which specialist path should handle the request.

#     This is intentionally rule-based for v1 because it is:
#     - predictable
#     - cheap
#     - easy to debug
#     - good enough for routing before we add LLM-based routing later
#     """
#     text = f"{user_text}\n{uploaded_text}".lower()

#     if (
#         CVE_PATTERN.search(text)
#         or any(hint in text for hint in VULN_HINTS)
#         or any(hint in text for hint in IOC_HINTS)
#     ):
#         return "threat_intel"

#     if any(hint in text for hint in DETECTION_HINTS):
#         return "detection"

#     if knowledge_base_ready or any(hint in text for hint in RAG_HINTS):
#         return "rag"

#     return "rag"

def classify_route(
    user_text: str,
    uploaded_text: str = "",
    knowledge_base_ready: bool = False,
) -> RouteType:

    text = f"{user_text}\n{uploaded_text}".lower()

    print("\nROUTER TEXT:")
    print(text)

    if (
        CVE_PATTERN.search(text)
        or IP_PATTERN.search(text)
        or URL_PATTERN.search(text)
        or HASH_PATTERN.search(text)
        or any(hint in text for hint in VULN_HINTS)
        or any(hint in text for hint in IOC_HINTS)
    ):
        print("ROUTE = threat_intel")
        return "threat_intel"

    if any(hint in text for hint in DETECTION_HINTS):
        print("ROUTE = detection")
        return "detection"

    if knowledge_base_ready or any(hint in text for hint in RAG_HINTS):
        print("ROUTE = rag")
        return "rag"

    print("ROUTE = rag")
    return "rag"
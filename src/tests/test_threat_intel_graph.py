from src.graph.subgraphs.threat_intel_subgraph import (
    build_threat_intel_subgraph
)

graph = build_threat_intel_subgraph()

state = {
    "user_text": """
Connection observed from 185.220.101.25.

User clicked:

hxxp://evilsite.com/login

File hash:

44d88612fea8a8f36de82e1278abb02f

Potential vulnerability:

CVE-2021-44228
"""
}

result = graph.invoke(state)

print()

print("========== FINAL REPORT ==========")

print()

print(result["final_answer"])
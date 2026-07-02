from src.graph.subgraphs.ioc_subgraph import build_ioc_subgraph

graph = build_ioc_subgraph()

state = {
    "user_text": """
Connection from 185.220.101.25
Email attacker@gmail.com
URL hxxp://evilsite.com/login
CVE-2021-44228
"""
}

result = graph.invoke(state)

print(result)
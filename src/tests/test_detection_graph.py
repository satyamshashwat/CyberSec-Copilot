from src.graph.subgraphs.detection_subgraph import (
    build_detection_subgraph
)

graph = build_detection_subgraph()

state = {
    "user_text":
    """
    PowerShell was used to perform brute force attacks.
    Multiple failed logins followed by successful login.
    """
}

result = graph.invoke(state)

print("\n========== FINAL RESULT ==========\n")

print(
    result["final_answer"]
)
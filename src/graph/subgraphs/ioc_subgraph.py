# IOC Subgraph
from langgraph.graph import StateGraph, START, END

from src.tools.extraction.ioc_extractor import extract_iocs
from src.core.llm import build_chat_model
from src.prompts.ioc_prompt import IOC_ANALYSIS_PROMPT


def extract_ioc_node(state):
    text = state["user_text"]

    iocs = extract_iocs(text)

    return {
        "extracted_iocs": iocs
    }


def analyze_ioc_node(state):

    llm = build_chat_model()

    prompt = f"""
{IOC_ANALYSIS_PROMPT}

IOCs:

{state["extracted_iocs"]}
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": {
            "title": "IOC Analysis",
            "summary": response.content,
            "possible_threat": "",
            "severity": "medium",
            "recommendations": [],
            "evidence": [],
            "confidence": 0.8
        }
    }


def build_ioc_subgraph():

    graph = StateGraph(dict)

    graph.add_node("extract_iocs", extract_ioc_node)
    graph.add_node("analyze_iocs", analyze_ioc_node)

    graph.add_edge(START, "extract_iocs")
    graph.add_edge("extract_iocs", "analyze_iocs")
    graph.add_edge("analyze_iocs", END)

    return graph.compile()
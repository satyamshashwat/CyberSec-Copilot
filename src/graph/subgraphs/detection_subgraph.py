from langgraph.graph import StateGraph, START, END
from typing import Any

from src.core.state import AppState
from src.core.llm import build_chat_model
from src.core.schemas import CybersecurityAnswer

from src.tools.detection.mitre_mapper import map_to_mitre
from src.tools.detection.sigma_generator import generate_sigma_rule
from src.tools.detection.yara_generator import generate_yara_rule

llm = build_chat_model()

def mitre_node(state: AppState):
    text = state["user_text"]
    techniques = map_to_mitre(text)
    print("\n===== MITRE NODE =====")
    print(techniques)
    return {"mitre_techniques": techniques}

def sigma_node(state: AppState):
    sigma_rule = generate_sigma_rule(state["user_text"])
    print("\n===== SIGMA NODE =====")
    print(sigma_rule)
    return {"sigma_rule": sigma_rule}

def yara_node(state: AppState):
    yara_rule = generate_yara_rule(state["user_text"])
    print("\n===== YARA NODE =====")
    print(yara_rule)
    return {"yara_rule": yara_rule}

def assessment_node(state: AppState):
    print("\n===== ASSESSMENT NODE =====")
    mitre_techs = state.get("mitre_techniques", [])
    sigma_rule = state.get("sigma_rule", "")
    yara_rule = state.get("yara_rule", "")
    
    prompt = f"""You are a detection engineer.
Analyze the following detection engineering artifacts and produce a structured analysis.

MITRE techniques:
{mitre_techs}

Sigma rule:
{sigma_rule}

YARA rule:
{yara_rule}

Synthesize a comprehensive structured response following the CybersecurityAnswer schema. Include the Sigma and YARA rules in the notes or evidence.
"""

    structured_llm = llm.with_structured_output(CybersecurityAnswer)
    result = structured_llm.invoke(prompt)
    
    # Let's ensure the Sigma/YARA rules are saved in the result's notes
    if hasattr(result, "notes") and isinstance(result.notes, list):
        if sigma_rule:
            result.notes.append(f"### Generated Sigma Rule\n```yaml\n{sigma_rule}\n```")
        if yara_rule:
            result.notes.append(f"### Generated YARA Rule\n```yara\n{yara_rule}\n```")
            
    # Convert result to dict
    if hasattr(result, "model_dump"):
        final_answer = result.model_dump()
    elif isinstance(result, dict):
        final_answer = result
    else:
        final_answer = {"summary": str(result)}
        
    return {"final_answer": final_answer}

def build_detection_subgraph():
    graph = StateGraph(AppState)
    
    graph.add_node("mitre", mitre_node)
    graph.add_node("sigma", sigma_node)
    graph.add_node("yara", yara_node)
    graph.add_node("assessment", assessment_node)
    
    graph.add_edge(START, "mitre")
    graph.add_edge("mitre", "sigma")
    graph.add_edge("sigma", "yara")
    graph.add_edge("yara", "assessment")
    graph.add_edge("assessment", END)
    
    return graph.compile()
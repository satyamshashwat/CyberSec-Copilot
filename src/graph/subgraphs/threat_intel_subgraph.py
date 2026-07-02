from langgraph.graph import StateGraph, START, END
from typing import Any

from src.core.state import AppState
from src.core.llm import build_chat_model
from src.core.schemas import CybersecurityAnswer

from src.tools.extraction.ioc_extractor import extract_iocs
from src.tools.threat_intel.virustotal_tool import (
    lookup_ip,
    lookup_domain,
    lookup_hash,
    lookup_url
)
from src.tools.threat_intel.abuseipdb_tool import lookup_ip_abuseipdb
from src.tools.threat_intel.urlscan_tool import (
    lookup_ip_urlscan,
    lookup_domain_urlscan,
    lookup_url_urlscan
)
from src.tools.threat_intel.nvd_tool import lookup_cve
from src.tools.threat_intel.misp_lookup import lookup_misp

llm = build_chat_model()

def extract_ioc_node(state: AppState):
    text = state["user_text"]
    iocs = extract_iocs(text)
    return {
        "extracted_iocs": iocs,
        "extracted_ips": iocs["ips"],
        "extracted_urls": iocs["urls"],
        "extracted_domains": iocs["domains"],
        "extracted_emails": iocs["emails"],
        "extracted_hashes": iocs["md5_hashes"] + iocs["sha1_hashes"] + iocs["sha256_hashes"],
        "extracted_cves": iocs["cves"]
    }

def virustotal_node(state: AppState):
    ips = state.get("extracted_ips", [])
    urls = state.get("extracted_urls", [])
    hashes = state.get("extracted_hashes", [])
    domains = state.get("extracted_domains", [])
    
    evidence = []
    for ip in ips:
        res = lookup_ip(ip)
        if res:
            evidence.append({"tool": "VirusTotal", "type": "ip", "data": res})
            
    for domain in domains:
        res = lookup_domain(domain)
        if res:
            evidence.append({"tool": "VirusTotal", "type": "domain", "data": res})
            
    for md5_hash in hashes:
        res = lookup_hash(md5_hash)
        if res:
            evidence.append({"tool": "VirusTotal", "type": "hash", "data": res})
            
    for url in urls:
        res = lookup_url(url)
        if res:
            evidence.append({"tool": "VirusTotal", "type": "url", "data": res})
            
    return {"vt_results": evidence}

def abuseipdb_node(state: AppState):
    ips = state.get("extracted_ips", [])
    evidence = []
    for ip in ips:
        res = lookup_ip_abuseipdb(ip)
        if res:
            evidence.append({"tool": "AbuseIPDB", "type": "ip", "data": res})
    return {"misp_results": state.get("misp_results", []), "evidence": state.get("evidence", []) + evidence}

def urlscan_node(state: AppState):
    ips = state.get("extracted_ips", [])
    domains = state.get("extracted_domains", [])
    urls = state.get("extracted_urls", [])
    
    evidence = []
    for ip in ips:
        res = lookup_ip_urlscan(ip)
        if res:
            evidence.append({"tool": "URLScan", "type": "ip", "data": res})
            
    for domain in domains:
        res = lookup_domain_urlscan(domain)
        if res:
            evidence.append({"tool": "URLScan", "type": "domain", "data": res})
            
    for url in urls:
        res = lookup_url_urlscan(url)
        if res:
            evidence.append({"tool": "URLScan", "type": "url", "data": res})
            
    return {"evidence": state.get("evidence", []) + evidence}

def misp_node(state: AppState):
    ips = state.get("extracted_ips", [])
    domains = state.get("extracted_domains", [])
    hashes = state.get("extracted_hashes", [])
    
    evidence = []
    for ip in ips:
        res = lookup_misp(ip)
        if res and "error" not in res:
            evidence.append({"tool": "MISP", "type": "ip", "data": res})
            
    for domain in domains:
        res = lookup_misp(domain)
        if res and "error" not in res:
            evidence.append({"tool": "MISP", "type": "domain", "data": res})
            
    for hash_value in hashes:
        res = lookup_misp(hash_value)
        if res and "error" not in res:
            evidence.append({"tool": "MISP", "type": "hash", "data": res})
            
    return {"misp_results": evidence}

def nvd_node(state: AppState):
    cves = state.get("extracted_cves", [])
    cve_results = []
    for cve in cves:
        res = lookup_cve(cve)
        if res:
            cve_results.append({"tool": "NVD", "type": "cve", "data": res})
    return {"nvd_results": cve_results}

def merge_node(state: AppState):
    evidence = []
    
    # VirusTotal
    evidence.extend(state.get("vt_results", []))
    # NVD
    evidence.extend(state.get("nvd_results", []))
    # MISP
    evidence.extend(state.get("misp_results", []))
    # Append any accumulated evidence from URLScan and AbuseIPDB
    evidence.extend(state.get("evidence", []))
    
    print("\n===== MERGE NODE =====")
    print("VirusTotal:", len(state.get("vt_results", [])))
    print("MISP:", len(state.get("misp_results", [])))
    print("NVD:", len(state.get("nvd_results", [])))
    print("Other:", len(state.get("evidence", [])))
    
    return {"evidence": evidence}

def assessment_node(state: AppState):
    evidence = state.get("evidence", [])
    
    prompt = f"""You are a senior SOC analyst.
Analyze the threat intelligence evidence below and synthesize a structured response.

User query/context:
{state.get("user_text", "")}

Extracted IOCs:
{state.get("extracted_iocs", {})}

Threat intelligence evidence:
{evidence}

Produce a structured output following the CybersecurityAnswer schema.
"""
    
    structured_llm = llm.with_structured_output(CybersecurityAnswer)
    result = structured_llm.invoke(prompt)
    
    # Convert result to dict
    if hasattr(result, "model_dump"):
        final_answer = result.model_dump()
    elif isinstance(result, dict):
        final_answer = result
    else:
        final_answer = {"summary": str(result)}
        
    return {"final_answer": final_answer}

def build_threat_intel_subgraph():
    graph = StateGraph(AppState)
    
    graph.add_node("extract_ioc", extract_ioc_node)
    graph.add_node("virustotal", virustotal_node)
    graph.add_node("abuseipdb", abuseipdb_node)
    graph.add_node("urlscan", urlscan_node)
    graph.add_node("misp", misp_node)
    graph.add_node("nvd", nvd_node)
    graph.add_node("merge", merge_node)
    graph.add_node("assessment", assessment_node)
    
    # Flow
    graph.add_edge(START, "extract_ioc")
    graph.add_edge("extract_ioc", "virustotal")
    graph.add_edge("virustotal", "abuseipdb")
    graph.add_edge("abuseipdb", "urlscan")
    graph.add_edge("urlscan", "misp")
    graph.add_edge("misp", "nvd")
    graph.add_edge("nvd", "merge")
    graph.add_edge("merge", "assessment")
    graph.add_edge("assessment", END)
    
    return graph.compile()

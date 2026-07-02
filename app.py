from __future__ import annotations

import streamlit as st
import os
import json

from pathlib import Path
from src.services.analysis_service import CybersecurityCopilotService
from src.core.settings import settings

st.markdown("""
<style>
[data-testid="stToolbar"] {
    display: none;
} 
footer {
    visibility: hidden;
}
#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Set page config for a wider, modern layout
st.set_page_config(
    page_title="CyberSec Copilot 🛡️",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern dark cybersecurity aesthetic
st.markdown("""
<style>
    /* Dark glassmorphism container styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    .report-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .severity-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
    }
    
    .severity-critical {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    .severity-high {
        background-color: rgba(249, 115, 22, 0.2);
        color: #f97316;
        border: 1px solid #f97316;
        box-shadow: 0 0 10px rgba(249, 115, 22, 0.3);
    }
    
    .severity-medium {
        background-color: rgba(234, 179, 8, 0.2);
        color: #eab308;
        border: 1px solid #eab308;
    }
    
    .severity-low {
        background-color: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid #22c55e;
    }
    
    /* Header decoration */
    .copilot-header {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Initialize service (not cached so it can be mutated after file ingestion)
if "service" not in st.session_state:
    st.session_state.service = CybersecurityCopilotService()
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

service = st.session_state.service

# Resolve absolute base path so temp dir always works regardless of CWD
APP_BASE = Path(__file__).resolve().parent

# Sidebar: Configuration and Knowledge Base Ingestion
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/security-shield.png", width=80)
    st.markdown("<h2 class='copilot-header'>CyberSec Control Center</h2>", unsafe_allow_html=True)
    st.write("Upload logs, configuration files, or security policy PDFs/text to ingest into the local vector store.")
    
    uploaded_file = st.file_uploader("Ingest Document / Policy / Log", type=["txt", "pdf", "log", "json", "csv"])
    if uploaded_file is not None:
        if st.button("🚀 Index Document"):
            with st.spinner(f"Processing & indexing '{uploaded_file.name}'..."):
                # Use absolute path so temp dir resolves correctly regardless of CWD
                temp_dir = APP_BASE / "storage" / "temp"
                temp_dir.mkdir(parents=True, exist_ok=True)
                temp_path = temp_dir / uploaded_file.name
                try:
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    service.ingest_file(str(temp_path))
                    st.session_state.indexed_files.append(uploaded_file.name)
                    st.success(f"✅ Successfully indexed **{uploaded_file.name}**! You can now query it in the main panel.")
                except Exception as e:
                    st.error(f"❌ Ingestion failed: {e}")
                    st.exception(e)
                finally:
                    if temp_path.exists():
                        os.remove(temp_path)
    
    # Show list of indexed files
    if st.session_state.indexed_files:
        st.markdown("**📚 Indexed Documents:**")
        for fname in st.session_state.indexed_files:
            st.markdown(f"- `{fname}`")

    st.markdown("---")
    st.markdown("### Supported Integrations")
    
    vt_status = "Checked 🟢" if settings.has_virustotal() else "Not Configured 🔴"
    abuse_status = "Checked 🟢" if settings.has_abuseipdb() else "Not Configured 🔴"
    urlscan_status = "Checked 🟢" if settings.has_urlscan() else "Not Configured 🔴"
    nvd_status = "Checked 🟢" if settings.has_nvd() else "Not Configured 🔴"
    misp_status = "Checked 🟢" if settings.has_misp() else "Not Configured 🔴"

    st.markdown(f"- **VirusTotal API**: {vt_status}")
    st.markdown(f"- **AbuseIPDB v2**: {abuse_status}")
    st.markdown(f"- **URLScan.io**: {urlscan_status}")
    st.markdown(f"- **NVD CVE REST API**: {nvd_status}")
    st.markdown(f"- **MISP Threat Intel**: {misp_status}")

# Main Page Layout
st.markdown("<h1 class='copilot-header'> 🛡️ CyberSec Copilot Dashboard</h1>", unsafe_allow_html=True)
st.write("Analyze security incidents, investigate suspicious IPs/URLs/CVEs, generate Sigma/YARA detection rules, or query security policies.")

# Prompt Area
user_text = st.text_area(
    "Input Security Event, Log Snippet, CVE ID, IP, URL, or Query:",
    placeholder="Example: Investigate IP 8.8.8.8 and URL http://malicious-site.com\nOR: Generate a Sigma rule for failed RDP login attempts\nOR: What is our policy on remote access credentials?",
    height=150
)

# Analyze Button
if st.button("🔍 Run Investigation"):
    if not user_text.strip():
        st.warning("Please input some text to analyze.")
    else:
        with st.spinner("Analyzing threat indicators & synthesizing context..."):
            try:
                result = service.analyze(user_text)
                st.subheader("🧭 Route Selected")
                route = result["active_route"]

                if route == "threat_intel":
                    st.success("🛡 Threat Intelligence Workflow")

                elif route == "detection":
                    st.info("🎯 Detection Engineering Workflow")

                elif route == "rag":
                    st.warning("📚 Knowledge Base (RAG)")
                
                st.subheader("⚙ Investigation Pipeline")
                pipeline = []
                if result.get("vt_results"):
                    pipeline.append("✅ VirusTotal")

                if result.get("nvd_results"):
                    pipeline.append("✅ NVD")

                if result.get("mitre_techniques"):
                    pipeline.append("✅ MITRE ATT&CK")

                if result.get("sigma_rule"):
                    pipeline.append("✅ Sigma Rule")

                if result.get("yara_rule"):
                    pipeline.append("✅ YARA Rule")

                if result.get("misp_results"):
                    pipeline.append("✅ MISP")

                pipeline.append("✅ Gemini Analysis")

                for item in pipeline:
                    st.write(item)

                st.markdown("---")
                st.subheader("🔎 Extracted Indicators")

                if result.get("extracted_ips"):
                    st.write("**IPs:**", result["extracted_ips"])

                if result.get("extracted_domains"):
                    st.write("**Domains:**", result["extracted_domains"])

                if result.get("extracted_urls"):
                    st.write("**URLs:**", result["extracted_urls"])

                if result.get("extracted_hashes"):
                    st.write("**Hashes:**", result["extracted_hashes"])

                if result.get("extracted_cves"):
                    st.write("**CVEs:**", result["extracted_cves"])
                
                st.subheader("🎯 Analysis Report")
                retrieved_docs = result.get("retrieved_docs", [])

                if retrieved_docs:
                    st.subheader("📚 Retrieved Knowledge")

                    for i, doc in enumerate(retrieved_docs, start=1):
                        st.markdown(f"**Document {i}**")

                        if isinstance(doc, dict):
                            st.write(doc.get("page_content", str(doc)))
                        else:
                            st.write(str(doc))

                if "vt_results" in result:
                    st.subheader("VirusTotal Results")
                    st.dataframe(result["vt_results"])
                    
                if "nvd_results" in result:
                    st.subheader("NVD Results")
                    st.dataframe(result["nvd_results"])

                if "mitre_techniques" in result:
                    st.subheader("MITRE ATT&CK")
                    st.dataframe(result["mitre_techniques"])

                if "sigma_rule" in result:
                    st.subheader("Sigma Rule")
                    st.code(result["sigma_rule"], language="yaml")
                    
                if "yara_rule" in result:
                    st.subheader("YARA Rule")
                    st.code(result["yara_rule"], language="text")
                
                # Check if the final answer is structured dict
                ans = result.get("final_answer", {})
                
                if isinstance(ans, dict):
                    # Severity Badge Styling
                    sev = ans.get("severity", "low").lower()
                    severity_class = f"severity-{sev}"
                    
                    st.markdown(f"""
                    <div class="report-card">
                        <span class="severity-badge {severity_class}">{sev} severity</span>
                        <h2>{ans.get('title', 'Security Analysis')}</h2>
                        <p style="font-size: 1.15rem; line-height: 1.6;">{ans.get('summary', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Layout columns for details
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        if ans.get("possible_threat"):
                            st.info(f"**Identified Threat Scenario:** {ans.get('possible_threat')}")
                        
                        # Display recommendations
                        recs = ans.get("recommendations", [])
                        if recs:
                            st.subheader("📋 Actionable Recommendations")
                            for rec in recs:
                                st.write(f"- {rec}")
                        
                        # Display notes/code blocks (e.g. Sigma, YARA)
                        notes = ans.get("notes", [])
                        if notes:
                            st.subheader("📝 Technical Notes & Rule Artifacts")
                            for note in notes:
                                st.markdown(note)
                                
                    with col2:
                        # Confidence Score
                        conf = ans.get("confidence", 0.0)
                        st.subheader("📊 Confidence Rating")
                        st.progress(conf)
                        st.write(f"Rating: **{int(conf * 100)}%**")
                        
                        # Indicators of Compromise
                        iocs = ans.get("iocs", [])
                        if iocs:
                            st.subheader("🔍 Extracted IOCs")
                            for ioc in iocs:
                                st.code(ioc, language="text")
                                
                        # Mapped MITRE techniques
                        mitre = ans.get("mitre_techniques", [])
                        if mitre:
                            st.subheader("🎗️ MITRE ATT&CK Mapping")
                            for tech in mitre:
                                st.markdown(f"- **{tech}**")
                                
                    # Raw Evidence Section
                    evidence = result.get("evidence", [])
                    if evidence:
                        with st.expander("🔬 View Collected Threat Intelligence Evidence"):
                            for idx, ev in enumerate(evidence):
                                tool = ev.get("tool", "Unknown")
                                ev_type = ev.get("type", "")
                                ev_data = ev.get("data", {})
                                st.markdown(f"#### {idx+1}. {tool} ({ev_type.upper()})")
                                st.json(ev_data)
                
                else:
                    # Fallback string display
                    st.markdown(ans)
                st.download_button(
                    label="📥 Download Full JSON Report",
                    data=json.dumps(result, indent=4),
                    file_name="cybersec_report.json",
                    mime="application/json",
                )

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.exception(e)

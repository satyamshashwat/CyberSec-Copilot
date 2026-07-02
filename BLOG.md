# Building an Agentic Cybersecurity Copilot: Leveraging LangGraph, RAG, and Threat Intel APIs

Modern Security Operations Center (SOC) analysts and incident responders face a dual crisis of **context-switching fatigue** and **information fragmentation**. Responding to an incident typically requires:

* Checking threat indicators (IPs, URLs, domains, file hashes) across multiple public/private databases (VirusTotal, AbuseIPDB, URLScan, NVD).
* Cross-referencing local findings with internal compliance frameworks and Standard Operating Procedures (SOPs).
* Mapping adversary behavior to threat matrix databases like MITRE ATT&CK.
* Manually writing detection engineering rules (Sigma, YARA) for the SIEM.

To solve this, I designed and built **CyberSec Copilot**—a fully functional, modular agentic AI application built using **LangGraph**, **ChromaDB**, and **Gemini**. The app operates as an intelligent orchestrator that routes user inputs to specialized analytical subgraphs and visualizes the investigation pipeline through a sleek Streamlit frontend.

---

## 🏛️ System Architecture Overview

Instead of running queries through a linear LLM prompt, the application uses **LangGraph's StateGraph** to manage states across three specialized subgraphs.

The diagram below shows the **complete workflow** — the top section shows the main router graph dispatching to each specialist subgraph, and the bottom section shows the internal node chains within each subgraph.

![CyberSec Copilot — Full LangGraph Architecture](combined_architecture_diagram.png)

---

## ⚙️ Deep Dive into the Subgraphs

### 1. The Threat Intelligence Subgraph

When the router detects threat indicators (IPs, domains, hashes, URLs, or CVEs), it triggers the **Threat Intel Workflow**.

* **IOC Extractor Node:** Uses regular expressions to extract unique indicator sets (MD5, SHA1, SHA256 hashes, IPv4s, domains, URLs, and CVE numbers) from raw input logs or alerts.
* **API Lookups:** Queries the configured databases sequentially, gathering JSON evidence.
* **State Merging:** The intermediate data points are parsed and appended to a unified `evidence` state array.
* **LLM Assessment:** A structured Gemini prompt parses the aggregated evidence and constructs a formal schema response matching a Pydantic `CybersecurityAnswer` class.

### 2. The Detection Engineering Subgraph

When the user asks for rules (e.g. *"Generate a detection rule for failed RDP login attempts"*):

* **MITRE ATT&CK Node:** Maps description keywords directly to technique IDs (e.g., matching "brute force" to `T1110`).
* **Sigma Generator Node:** Generates YAML-formatted SIEM detection rules.
* **YARA Generator Node:** Generates text-based file/process signature detection rules.
* **Assessment Node:** Synthesizes the final report and embeds the code blocks in a markdown layout.

### 3. The RAG Subgraph (Knowledge Base)

To retrieve local context from standard policies (like compliance documentation, internal guides, or past incident logs):

* **Document Ingestion:** Handled by [indexer.py](file:///c:/Users/KIIT0001/Documents/CyberAssistant/cybersec-copilot/src/ingestion/indexer.py). When a document (PDF, TXT, LOG, CSV, or JSON) is uploaded, it is parsed, broken down into chunks with a text splitter, embedded using Google GenAI Embeddings, and stored in a local persistent directory under `storage/vectorstore/cyber_kb` via Chroma.
* **Context Retrieval:** Queries the Chroma store for the top 4 most relevant chunks, serializes them, and builds a comprehensive system prompt for the Gemini LLM.

---

## 🛡️ Software Resiliency & Failure Tolerance

A critical aspect of building software that integrates with external APIs is handling network failures and latency. During development, we encountered a common pitfall with **MISP** (Malware Information Sharing Platform).

### The Problem: Global Initialization Crash

Initially, the PyMISP client was instantiated globally in [misp_lookup.py](file:///c:/Users/KIIT0001/Documents/CyberAssistant/cybersec-copilot/src/tools/threat_intel/misp_lookup.py):

```python
# CRITICAL ERRORS: Fails at startup if localhost/remote MISP is offline
misp = ExpandedPyMISP(MISP_URL, MISP_API_KEY, ssl=False)
```

If the MISP server was offline or set to a placeholder like `https://localhost`, Python's module loader threw an exception during import time, crashing the entire dashboard immediately.

### The Solution: Functional Initialization & Exception Shielding

To make the application robust, we restructured the code to instantiate PyMISP dynamically inside the lookup functions, catching all connection errors:

```python
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def lookup_misp(value: str):
    load_dotenv()
    misp_url = os.getenv("MISP_URL")
    misp_api_key = os.getenv("MISP_API_KEY")
  
    if not misp_url or not misp_api_key:
        return {"error": "MISP server not configured in .env."}
      
    try:
        from pymisp import PyMISP
        # Mute verbose logs to keep CLI output clean
        logging.getLogger("pymisp").setLevel(logging.WARNING)
      
        misp = PyMISP(misp_url, misp_api_key, ssl=False)
        result = misp.search(value=value, pythonify=False, controller="attributes")
        return result
    except Exception as e:
        logger.warning(f"MISP lookup failed: {e}")
        return {"error": str(e)}
```

Now, if a user's MISP database is offline or not configured, the copilot logs a warning and proceeds to generate recommendations based on remaining tools like VirusTotal, ensuring zero downtime.

---

## 🎨 Interactive Security Dashboard (Streamlit)

The UI is built using Streamlit, styled with a custom dark-mode cybersecurity theme featuring:

1. **Dynamic Supported Integrations Sidebar:** Reads the `.env` settings directly to check which tools are active and outputs a visual checklist (e.g. **VirusTotal API: Checked 🟢** or **MISP Threat Intel: Not Configured 🔴**).
2. **Dynamic Route Selected Banner:** Highlights which specialist path (Threat Intel, Detection, or RAG) the Supervisor Graph selected.
3. **Investigation Pipeline Visualizer:** Outputs a step-by-step audit checklist showing which nodes ran successfully (e.g. `✅ VirusTotal`, `✅ MITRE ATT&CK`, `✅ Gemini Analysis`).
4. **Dataframes & Structured Rules:** Shows structured tables of threat lookups and formatting for Sigma / YARA rules using syntax-highlighted code blocks.
5. **Downloadable Reports:** Allows analysts to download the entire investigation output array as a single JSON report file (`cybersec_report.json`) for ticketing system documentation.

---

## 🚀 Setting Up the Project

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure Your Environment (`.env`)

Create a `.env` file in the root workspace:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash

# Threat Intel APIs
VIRUSTOTAL_API_KEY=your_vt_api_key
ABUSEIPDB_API_KEY=your_abuse_api_key
URLSCAN_API_KEY=your_urlscan_api_key
NVD_API_KEY=your_nvd_api_key

# MISP Server settings
MISP_URL=https://your-misp-server-address
MISP_API_KEY=your_misp_key
```

### 3. Launch the Application

```powershell
streamlit run app.py
```

---

## 📈 Future Scope

1. **SOAR Integration:** Adding downstream actions, such as triggering webhook playbooks (e.g., auto-creating a Jira ticket or isolating a host using CrowdStrike Falcon).
2. **Local LLM Execution:** Switching the graph routing and synthesis nodes to run on local llama3 models via Ollama to allow offline execution in zero-trust networks.

By combining agentic state graphs with RAG and unified threat lookups, the CyberSec Copilot streamlines triage and provides actionable reports in seconds.

---

*Got questions or feedback on building security co-pilots? Leave your comments below or check out the code repository!*
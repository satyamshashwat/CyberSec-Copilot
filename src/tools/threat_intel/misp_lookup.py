import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def lookup_misp(value: str):
    """
    Search MISP server for threat intelligence.
    """
    load_dotenv()
    misp_url = os.getenv("MISP_URL")
    misp_api_key = os.getenv("MISP_API_KEY")
    
    if not misp_url or not misp_api_key:
        return {"error": "MISP server not configured in .env."}
        
    try:
        from pymisp import PyMISP
        # Disable logging for pymisp to keep terminal clean
        logging.getLogger("pymisp").setLevel(logging.WARNING)
        
        misp = PyMISP(misp_url,misp_api_key,ssl=False)
        result = misp.search(value=value,pythonify=False,controller="attributes")
        return result
    except ImportError:
        return {"error": "pymisp package not installed."}
    except Exception as e:
        logger.warning(f"MISP lookup failed: {e}")
        return {"error": str(e)}

def test_connection():
    load_dotenv()
    misp_url = os.getenv("MISP_URL")
    misp_api_key = os.getenv("MISP_API_KEY")
    
    if not misp_url or not misp_api_key:
        return {"error": "MISP server not configured in .env."}
        
    try:
        from pymisp import PyMISP
        # Disable logging for pymisp to keep terminal clean
        logging.getLogger("pymisp").setLevel(logging.WARNING)
        
        misp = PyMISP(misp_url,misp_api_key,ssl=False)
        return {"connected": True,"version": misp.misp_instance_version}
    except Exception as e:
        return {"error": f"Failed to connect to MISP: {e}"}
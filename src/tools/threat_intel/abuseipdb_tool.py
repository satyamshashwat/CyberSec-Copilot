import requests
from src.core.settings import settings

def lookup_ip_abuseipdb(ip: str):
    """
    Look up IP reputation from AbuseIPDB API v2.
    """
    api_key = settings.abuseipdb_api_key
    if not api_key:
        return {"error": "AbuseIPDB API key not configured in .env."}
    
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return {"error": f"AbuseIPDB API returned status {response.status_code}: {response.text}"}
        
        data = response.json().get("data", {})
        return {
            "ip": ip,
            "abuseConfidenceScore": data.get("abuseConfidenceScore", 0),
            "countryCode": data.get("countryCode", ""),
            "usageType": data.get("usageType", ""),
            "isp": data.get("isp", ""),
            "domain": data.get("domain", ""),
            "totalReports": data.get("totalReports", 0),
            "isWhitelisted": data.get("isWhitelisted", False)
        }
    except Exception as e:
        return {"error": f"AbuseIPDB lookup failed: {str(e)}"}

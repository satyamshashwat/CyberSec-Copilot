import requests
from src.core.settings import settings

def search_urlscan(query: str):
    """
    Search urlscan.io historical database for a query.
    """
    api_key = settings.urlscan_api_key
    if not api_key:
        return {"error": "URLScan API key not configured in .env."}
    
    url = f"https://urlscan.io/api/v1/search/?q={query}"
    headers = {
        "API-Key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"URLScan API returned status {response.status_code}: {response.text}"}
        
        data = response.json()
        results = data.get("results", [])
        if not results:
            return {"query": query, "found": False}
        
        summaries = []
        for r in results[:3]:
            page = r.get("page", {})
            task = r.get("task", {})
            verdicts = r.get("verdicts", {})
            summaries.append({
                "domain": page.get("domain"),
                "url": page.get("url"),
                "server": page.get("server"),
                "ip": page.get("ip"),
                "time": task.get("time"),
                "score": verdicts.get("overall", {}).get("score", 0),
                "malicious": verdicts.get("overall", {}).get("malicious", False),
            })
        return {
            "query": query,
            "found": True,
            "results": summaries
        }
    except Exception as e:
        return {"error": f"URLScan search failed: {str(e)}"}

def lookup_domain_urlscan(domain: str):
    return search_urlscan(f"domain:{domain}")

def lookup_ip_urlscan(ip: str):
    return search_urlscan(f"ip:{ip}")

def lookup_url_urlscan(url_val: str):
    # Free tier key does not support searching the 'url' field. 
    # Fall back to extracting the domain and performing a domain search.
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url_val)
        domain = parsed.netloc or parsed.path
        if ":" in domain:
            domain = domain.split(":")[0]
        if domain:
            return lookup_domain_urlscan(domain)
    except Exception:
        pass
    return search_urlscan(f"url:\"{url_val}\"")


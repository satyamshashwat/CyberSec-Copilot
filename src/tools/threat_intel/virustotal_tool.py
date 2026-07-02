# VirusTotal Tool
import os
import requests
import base64
from dotenv import load_dotenv
load_dotenv()
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
# VT_API_KEY = "5721159a62c771f264abb8d185091c41226336edee20a273b21c3eeb6669d326"

HEADERS = {
    "x-apikey": VT_API_KEY
}


def lookup_ip(ip: str):

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return {
            "error": response.text
        }

    data = response.json()

    stats = data["data"]["attributes"]["last_analysis_stats"]

    return {
        "ip": ip,
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "harmless": stats["harmless"]
    }



def lookup_domain(domain: str):

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return {
            "error": response.text
        }

    data = response.json()

    stats = data["data"]["attributes"]["last_analysis_stats"]

    return {
        "domain": domain,
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "harmless": stats["harmless"]
    }

def lookup_hash(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    stats = data["data"]["attributes"]["last_analysis_stats"]

    return {
        "hash": file_hash,
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "harmless": stats["harmless"]
    }    

def lookup_url(url_value):

    url_id = base64.urlsafe_b64encode(
        url_value.encode()
    ).decode().strip("=")

    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    stats = data["data"]["attributes"]["last_analysis_stats"]

    return {
        "url": url_value,
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "harmless": stats["harmless"]
    }    
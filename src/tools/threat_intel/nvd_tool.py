# NVD Tool
import os
import requests

API_KEY = os.getenv("NVD_API_KEY")


def lookup_cve(cve_id: str):

    url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0"
    )

    headers = {}

    if API_KEY:
        headers["apiKey"] = API_KEY

    params = {
        "cveId": cve_id
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        return {
            "error": response.text
        }

    vulnerabilities = response.json()["vulnerabilities"]

    if not vulnerabilities:
        return {
            "cve": cve_id,
            "found": False
        }

    cve_data = vulnerabilities[0]["cve"]

    description = cve_data["descriptions"][0]["value"]

    return {
        "cve": cve_id,
        "description": description
    }
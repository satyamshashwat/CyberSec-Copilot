# IOC Extractor
import re


def extract_iocs(text: str) -> dict:
    """
    Extract Indicators of Compromise (IOCs) from text.
    """

    # IPv4 addresses
    ips = re.findall(
        r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
        text
    )

    # URLs
    urls = re.findall(
        r"(?:https?|hxxp)://[^\s]+",
        text,
        flags=re.IGNORECASE
    )

    # Domains
    domains = re.findall(
        r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b",
        text
    )

    # Emails
    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    # MD5 hashes (32 chars)
    md5_hashes = re.findall(
        r"\b[a-fA-F0-9]{32}\b",
        text
    )

    # SHA1 hashes (40 chars)
    sha1_hashes = re.findall(
        r"\b[a-fA-F0-9]{40}\b",
        text
    )

    # SHA256 hashes (64 chars)
    sha256_hashes = re.findall(
        r"\b[a-fA-F0-9]{64}\b",
        text
    )

    # CVEs
    cves = re.findall(
        r"CVE-\d{4}-\d+",
        text,
        flags=re.IGNORECASE
    )

    return {
        "ips": list(set(ips)),
        "urls": list(set(urls)),
        "domains": list(set(domains)),
        "emails": list(set(emails)),
        "md5_hashes": list(set(md5_hashes)),
        "sha1_hashes": list(set(sha1_hashes)),
        "sha256_hashes": list(set(sha256_hashes)),
        "cves": list(set(cves))
    }
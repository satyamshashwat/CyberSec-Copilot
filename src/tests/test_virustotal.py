# from dotenv import load_dotenv

# load_dotenv()

# from src.tools.threat_intel.virustotal_tool import lookup_ip


# result = lookup_ip(
#     "8.8.8.8"
# )

# print(result)

from dotenv import load_dotenv

load_dotenv()

from src.tools.threat_intel.virustotal_tool import (
    lookup_ip,
    lookup_domain,
    lookup_hash,
    lookup_url
)

print("\n===== IP Lookup =====")
print(
    lookup_ip("185.220.101.25")
)

print("\n===== Domain Lookup =====")
print(
    lookup_domain("google.com")
)

print("\n===== Hash Lookup =====")
print(
    lookup_hash(
        "44d88612fea8a8f36de82e1278abb02f"
    )
)

print("\n===== URL Lookup =====")
print(
    lookup_url(
        "http://example.com"
    )
)
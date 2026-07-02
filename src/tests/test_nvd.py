from src.tools.threat_intel.nvd_tool import lookup_cve

result = lookup_cve(
    "CVE-2021-44228"
)

print(result)
from src.tools.detection.mitre_mapper import map_to_mitre

result = map_to_mitre(
    "PowerShell was used for brute force attacks"
)

print(result)
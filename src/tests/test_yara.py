from src.tools.detection.yara_generator import generate_yara_rule

print(
    generate_yara_rule(
        "Malware using powershell.exe and cmd.exe"
    )
)
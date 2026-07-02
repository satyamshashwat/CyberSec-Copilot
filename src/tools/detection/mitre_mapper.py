# MITRE ATT&CK Mapper

MITRE_TECHNIQUES = {
    "powershell": {
        "id": "T1059.001",
        "name": "PowerShell"
    },

    "cmd.exe": {
        "id": "T1059.003",
        "name": "Windows Command Shell"
    },

    "brute force": {
        "id": "T1110",
        "name": "Brute Force"
    },

    "credential dumping": {
        "id": "T1003",
        "name": "Credential Dumping"
    },

    "ransomware": {
        "id": "T1486",
        "name": "Data Encrypted for Impact"
    },

    "phishing": {
        "id": "T1566",
        "name": "Phishing"
    }
}


def map_to_mitre(text: str):

    text = text.lower()

    techniques = []

    for keyword, technique in MITRE_TECHNIQUES.items():

        if keyword in text:

            techniques.append(
                technique
            )

    return techniques

# def mitre_node(state: AppState):

#     text = state["user_text"]

#     techniques = map_to_mitre(text)

#     print("\n===== MITRE NODE =====")
#     print(techniques)

#     return {
#         "mitre_techniques": techniques
#     }
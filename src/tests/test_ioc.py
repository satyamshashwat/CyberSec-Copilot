# # Test IOC
# from src.tools.extraction.ioc_extractor import extract_iocs


# sample_text = """
# Suspicious connection from 185.220.101.25

# Malicious URL:
# hxxp://evilsite.com/login

# Email:
# attacker@gmail.com

# MD5:
# 44d88612fea8a8f36de82e1278abb02f

# Related vulnerability:
# CVE-2021-44228
# """


# result = extract_iocs(sample_text)

# print(result)


from src.graph.subgraphs.ioc_subgraph import build_ioc_subgraph

graph = build_ioc_subgraph()

state = {
    "user_text": """
Connection from 185.220.101.25
Email attacker@gmail.com
URL hxxp://evilsite.com/login
CVE-2021-44228
"""
}

result = graph.invoke(state)

print(result)
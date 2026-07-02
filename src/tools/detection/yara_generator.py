from src.core.llm import build_chat_model

llm = build_chat_model()


def generate_yara_rule(description: str):

    prompt = f"""
You are a malware analyst.

Generate a YARA rule for:

{description}

Return only YARA code.
"""

    response = llm.invoke(prompt)

    return response.content
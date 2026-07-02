from src.core.llm import build_chat_model

llm = build_chat_model()


def generate_sigma_rule(description: str):

    prompt = f"""
You are a Sigma detection engineer.

Generate a Sigma rule for:

{description}

Return only YAML.
"""

    response = llm.invoke(prompt)

    return response.content
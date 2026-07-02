from __future__ import annotations

import os
from langchain_google_genai import ChatGoogleGenerativeAI

from src.core.settings import settings


def build_chat_model(temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """
    Build the Gemini chat model used by the supervisor and specialist subgraphs.

    This module keeps model creation in one place so later we can swap:
    - models
    - temperature
    - provider settings
    - tracing / logging behavior
    without touching business logic.
    """
    if not settings.google_api_key:
        raise ValueError(
            "Missing GOOGLE_API_KEY or GEMINI_API_KEY. Set it in your .env file."
        )

    os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)

    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=temperature,
    )
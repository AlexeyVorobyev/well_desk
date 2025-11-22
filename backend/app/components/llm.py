"""LangChain or LLM-related components.

This module contains a minimal stub for generating assistant replies.
The implementation can be replaced with a real LLM integration using the
provided OpenAI-compatible API key from settings.
"""

from app.settings import get_settings


settings = get_settings()


def build_assistant_reply(user_message: str) -> str:
    """Return a deterministic assistant reply for the provided message."""

    if not user_message.strip():
        return ""

    # Placeholder generation logic; can be swapped for a real LLM call.
    intro = "Спасибо за сообщение!"
    summary = f"Вы написали: {user_message.strip()}"
    return f"{intro} {summary}"

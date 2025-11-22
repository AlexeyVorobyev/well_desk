"""LangChain or LLM-related components."""

from __future__ import annotations

from typing import Iterable, Sequence

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.models import Message, Wellbeing
from app.settings import get_settings


settings = get_settings()


SYSTEM_PROMPT = """
Ты — агент Well Desk. Давай короткие и практичные рекомендации по:
- снижению усталости и поддержанию продуктивности;
- разгрузке спины и шеи при работе за столом;
- поддержанию здоровья глаз в течение рабочего дня;
- простым оздоровительным практикам, которые легко внедрить.

Используй всю историю переписки и текущие показатели wellbeing. Делай ответы дружелюбными,
опирайся на настроение пользователя и его состояние. Предлагай конкретные действия или
мини-планы на ближайшее время, избегай медицинских диагнозов или советов, требующих
профессионального вмешательства.
"""


def _format_wellbeing(wellbeing: Wellbeing | None) -> str:
    if wellbeing is None:
        return "Данные wellbeing отсутствуют. Дай универсальные рекомендации."

    note = wellbeing.note.strip() if wellbeing.note else "Без заметок"
    return (
        "Текущий wellbeing: "
        f"energy={wellbeing.energy}/5, "
        f"stress={wellbeing.stress}/5, "
        f"focus={wellbeing.focus}/5, "
        f"mood={wellbeing.mood}. "
        f"Заметка: {note}. Обновлено: {wellbeing.updated_at.isoformat()}."
    )


def _serialize_history(messages: Iterable[Message]) -> list[BaseMessage]:
    history: list[BaseMessage] = []
    for message in messages:
        if message.role == "assistant":
            history.append(AIMessage(content=message.content))
        else:
            history.append(HumanMessage(content=message.content))
    return history


async def build_assistant_reply(messages: Sequence[Message], wellbeing: Wellbeing | None) -> str:
    """Generate an assistant reply using an OpenAI-compatible chat model via LangChain."""

    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    chat = ChatOpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
        temperature=0.4,
    )

    system_message = SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{_format_wellbeing(wellbeing)}")
    history = _serialize_history(messages)

    response = await chat.ainvoke([system_message, *history])
    return response.content.strip()

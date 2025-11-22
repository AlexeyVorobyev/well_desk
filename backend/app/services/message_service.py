from sqlalchemy.ext.asyncio import AsyncSession

from app.components.llm import build_assistant_reply
from app.dto import LLMMessageInput, MessageUserInput
from app.repositories import message_repository, profile_repository, wellbeing_repository


DEFAULT_USER_ID = profile_repository.DEFAULT_USER_ID


async def list_messages(session: AsyncSession):
    return await message_repository.list_messages(session)


async def create_user_message(session: AsyncSession, payload: MessageUserInput):
    content = payload.content.strip()
    if not content:
        raise ValueError("Message content cannot be empty")

    message = await message_repository.create_message(
        session,
        user_id=DEFAULT_USER_ID,
        role="user",
        content=content,
    )
    await session.commit()
    await session.refresh(message)
    return message


async def create_assistant_message(session: AsyncSession, payload: LLMMessageInput):
    source_message = await message_repository.get_message(session, payload.user_message_id)

    if source_message is None:
        raise LookupError("User message not found")

    if source_message.role != "user":
        raise ValueError("Provided message is not a user message")

    conversation = await message_repository.list_messages(session)
    wellbeing = await wellbeing_repository.get_wellbeing(session)

    reply_content = await build_assistant_reply(conversation, wellbeing)

    message = await message_repository.create_message(
        session,
        user_id=DEFAULT_USER_ID,
        role="assistant",
        content=reply_content,
        reply_to_id=source_message.id,
    )
    await session.commit()
    await session.refresh(message)
    return message

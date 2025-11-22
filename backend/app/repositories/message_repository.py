from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Message


async def list_messages(session: AsyncSession) -> List[Message]:
    result = await session.execute(select(Message).order_by(Message.created_at.asc()))
    return list(result.scalars().all())


async def get_message(session: AsyncSession, message_id: int) -> Optional[Message]:
    return await session.get(Message, message_id)


async def create_message(
    session: AsyncSession,
    *,
    user_id: str,
    role: str,
    content: str,
    reply_to_id: Optional[int] = None,
) -> Message:
    message = Message(user_id=user_id, role=role, content=content, reply_to_id=reply_to_id)
    session.add(message)
    await session.flush()
    return message

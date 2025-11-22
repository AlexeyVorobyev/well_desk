from sqlalchemy.orm import Session

from app.components.llm import build_assistant_reply
from app.dto import LLMMessageInput, MessageUserInput
from app.repositories import message_repository, profile_repository


DEFAULT_USER_ID = profile_repository.DEFAULT_USER_ID


def list_messages(session: Session):
    return message_repository.list_messages(session)


def create_user_message(session: Session, payload: MessageUserInput):
    content = payload.content.strip()
    if not content:
        raise ValueError("Message content cannot be empty")

    return message_repository.create_message(
        session,
        user_id=DEFAULT_USER_ID,
        role="user",
        content=content,
    )


def create_assistant_message(session: Session, payload: LLMMessageInput):
    source_message = message_repository.get_message(session, payload.user_message_id)

    if source_message is None:
        raise LookupError("User message not found")

    if source_message.role != "user":
        raise ValueError("Provided message is not a user message")

    reply_content = build_assistant_reply(source_message.content)

    return message_repository.create_message(
        session,
        user_id=DEFAULT_USER_ID,
        role="assistant",
        content=reply_content,
        reply_to_id=source_message.id,
    )

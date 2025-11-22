from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Message


def list_messages(session: Session) -> List[Message]:
    return session.query(Message).order_by(Message.created_at.asc()).all()


def get_message(session: Session, message_id: int) -> Optional[Message]:
    return session.query(Message).filter_by(id=message_id).one_or_none()


def create_message(
    session: Session,
    *,
    user_id: str,
    role: str,
    content: str,
    reply_to_id: Optional[int] = None,
) -> Message:
    message = Message(user_id=user_id, role=role, content=content, reply_to_id=reply_to_id)
    session.add(message)
    session.flush()
    return message

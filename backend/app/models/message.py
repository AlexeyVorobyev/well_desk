from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.components.database import Base


class Message(Base):
    """Represents a chat message authored by a user or assistant."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user_profile.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    reply_to_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

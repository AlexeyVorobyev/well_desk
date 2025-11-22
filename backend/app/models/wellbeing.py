from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.components.database import Base


class Wellbeing(Base):
    """Stores the current wellbeing state for a user."""

    __tablename__ = "wellbeing"

    user_id = Column(String, primary_key=True)
    energy = Column(Integer, nullable=False)
    stress = Column(Integer, nullable=False)
    focus = Column(Integer, nullable=False)
    mood = Column(String, nullable=False)
    note = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

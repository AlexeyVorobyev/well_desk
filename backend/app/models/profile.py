from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.components.database import Base


class UserProfile(Base):
    """Represents the single user profile stored in the system."""

    __tablename__ = "user_profile"

    id = Column(String, primary_key=True)
    age = Column(Integer, nullable=True)
    role = Column(String, nullable=True)
    work_style = Column(String, nullable=True)
    work_hours_from = Column(String, nullable=True)
    work_hours_to = Column(String, nullable=True)
    break_interval_minutes = Column(Integer, nullable=True)
    screen_break_preference = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

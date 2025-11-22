from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.components.database import Base


class MedicationReminder(Base):
    """Stores reminder configuration for medication intake."""

    __tablename__ = "medication_reminders"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    time = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    logs = relationship(
        "MedicationLog", back_populates="reminder", cascade="all, delete-orphan"
    )


class MedicationLog(Base):
    """Stores completion logs for reminders."""

    __tablename__ = "medication_logs"

    id = Column(String, primary_key=True)
    reminder_id = Column(String, ForeignKey("medication_reminders.id"), nullable=False)
    taken = Column(Boolean, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    reminder = relationship("MedicationReminder", back_populates="logs")

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MedicationReminderInput(BaseModel):
    title: str = Field(..., min_length=1)
    time: str = Field(..., regex=r"^\d{2}:\d{2}$")
    frequency: str = Field(..., min_length=1)


class MedicationReminder(BaseModel):
    id: str
    title: str
    time: str
    frequency: str
    created_at: datetime

    class Config:
        orm_mode = True


class MedicationLogInput(BaseModel):
    taken: bool


class MedicationLog(BaseModel):
    id: str
    reminder_id: str
    taken: bool
    timestamp: datetime
    reminder_title: Optional[str] = None
    reminder_time: Optional[str] = None

    class Config:
        orm_mode = True

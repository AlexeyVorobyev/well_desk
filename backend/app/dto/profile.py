from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserProfileInput(BaseModel):
    age: Optional[int] = Field(default=None)
    role: Optional[str] = Field(default=None)
    work_style: Optional[str] = Field(default=None)
    work_hours_from: Optional[str] = Field(default=None, description="HH:MM start time")
    work_hours_to: Optional[str] = Field(default=None, description="HH:MM end time")
    break_interval_minutes: Optional[int] = Field(default=None)
    screen_break_preference: Optional[str] = Field(default=None)


class UserProfile(UserProfileInput):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

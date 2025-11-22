from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class WellbeingInput(BaseModel):
    energy: int = Field(..., ge=1, le=5)
    stress: int = Field(..., ge=1, le=5)
    focus: int = Field(..., ge=1, le=5)
    mood: str
    note: Optional[str] = None

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("mood must not be empty")
        return value


class Wellbeing(WellbeingInput):
    updated_at: datetime

    class Config:
        orm_mode = True

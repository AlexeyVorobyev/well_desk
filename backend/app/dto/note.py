from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(..., max_length=200, description="Title of the note")
    content: str = Field(..., description="Body of the note")


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    summary: str | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: int
    role: Literal["user", "assistant"]
    content: str
    reply_to_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


class MessageUserInput(BaseModel):
    content: str = Field(..., min_length=1)


class LLMMessageInput(BaseModel):
    user_message_id: int = Field(..., ge=1)

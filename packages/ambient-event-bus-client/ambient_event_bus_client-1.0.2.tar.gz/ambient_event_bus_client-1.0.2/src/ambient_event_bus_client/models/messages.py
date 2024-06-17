from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    topic: str
    message: str


class Message(MessageCreate):
    id: int

    connection_id: int
    session_id: int

    timestamp: datetime
    created_at: datetime

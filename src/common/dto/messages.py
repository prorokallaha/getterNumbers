from typing import Optional

from pydantic import BaseModel


class MessagesCreate(BaseModel):
    id: int
    user_id: int
    message: Optional[str] = None


class MessageUpdate(BaseModel):
    user_id: int
    message: Optional[str] = None

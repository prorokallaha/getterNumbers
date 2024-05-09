from typing import Optional

from pydantic import BaseModel, Field


class CommandCreate(BaseModel):
    tag: Optional[str] = None
    text: Optional[str] = None
    image_item_id: Optional[str] = None


class CommandUpdate(BaseModel):
    tag: Optional[str] = None
    text: Optional[str] = None
    image_item_id: Optional[str] = None

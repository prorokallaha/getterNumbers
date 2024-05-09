from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):

    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


class UserUpdate(BaseModel):

    is_bot: Optional[bool] = None
    first_name: Optional[str] = None
    username: Optional[str] = None
    number: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None

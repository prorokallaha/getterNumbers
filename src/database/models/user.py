from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithTimeMixin


class User(Base, ModelWithTimeMixin):

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
    )
    is_bot: Mapped[bool]
    first_name: Mapped[str]
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_premium: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    added_to_attachment_menu: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_join_groups: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_read_all_group_messages: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    supports_inline_queries: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

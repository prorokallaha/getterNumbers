from typing import Optional

from sqlalchemy import (
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithIDMixin:
    """Base model class that represents ID with an integer type"""

    id: Mapped[Optional[int]] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )


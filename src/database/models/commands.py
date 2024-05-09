from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from src.database.models.base.mixins.with_id import ModelWithIDMixin
from src.database.models.base import Base


class Commands(Base):
    __tablename__ = 'commands'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(nullable=False, default=None, unique=True)
    text: Mapped[str] = mapped_column(nullable=False, default=None)
    image_item_id: Mapped[str] = mapped_column(String, nullable=True)

from sqlalchemy import (
    BigInteger,
    Boolean,
    String,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithTimeMixin


class Messages(ModelWithTimeMixin, Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship("User", back_populates="messages")
    message: Mapped[str] = mapped_column(nullable=True)

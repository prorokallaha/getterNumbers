from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.interfaces.repository import Repository
from src.database.repositories.crud import ModelType, SQLAlchemyCRUDRepository

RepositoryType = TypeVar("RepositoryType", bound=Repository)


class BaseRepository(Repository, Generic[ModelType]):
    __slots__ = (
        "model",
        "_session",
        "_crud",
    )
    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = SQLAlchemyCRUDRepository(session, self.model)

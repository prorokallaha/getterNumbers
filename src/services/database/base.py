import abc
from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.crud import ModelT, SQLAlchemyCRUDRepository


class BaseDBService(abc.ABC, Generic[ModelT]):

    model: Type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = SQLAlchemyCRUDRepository(session, self.model)

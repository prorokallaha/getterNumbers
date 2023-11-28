import abc
from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database.interfaces.repositories.crud import AbstractCRUDRepository
from src.database.repositories.crud import ModelT


class BaseService(abc.ABC, Generic[ModelT]):

    model: Type[ModelT]

    def __init__(
            self,
            crud_repo: AbstractCRUDRepository[AsyncSession, ModelT]
    ) -> None:
        self._crud_repo = crud_repo

import abc
from typing import Generic, Type

from src.common.database.interfaces.repositories.crud import AbstractCRUDRepository
from src.common.types import SessionType
from src.database.repositories.crud import ModelT


class BaseService(abc.ABC, Generic[SessionType, ModelT]):

    model: Type[ModelT]

    def __init__(
            self,
            crud_repo: AbstractCRUDRepository[SessionType, ModelT]
    ) -> None:
        self._crud_repo = crud_repo

    @property
    def session(self) -> SessionType:
        return self._crud_repo._session

import abc
from typing import Any, Generic, Protocol, Type

from src.common.database.interfaces.repositories.crud import AbstractCRUDRepository
from src.common.types import EntryType, SessionType


class ServiceType(Protocol):

    def __init__(
            self,
            crud_repo: AbstractCRUDRepository[SessionType, EntryType]
    ) -> None:
        raise NotImplementedError

    @property
    def session(self) -> Any:
        raise NotImplementedError

    @property
    def model(self) -> Type[Any]:
        raise NotImplementedError


class AbstractService(abc.ABC, Generic[SessionType, EntryType]):

    def __init__(
            self,
            crud_repo: AbstractCRUDRepository[SessionType, EntryType]
    ) -> None:
        self._crud_repo = crud_repo

    @property
    def session(self) -> SessionType:
        return self._crud_repo._session

    @property
    def model(self) -> Type[EntryType]:
        return self._crud_repo.model

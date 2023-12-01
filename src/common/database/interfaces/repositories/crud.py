from __future__ import annotations

import abc
from typing import (
    Any,
    Dict,
    Generic,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from src.common.types import EntryType, SessionType

T = TypeVar('T')

class AbstractCRUDRepository(
    abc.ABC, Generic[SessionType, EntryType]
):

    def __init__(self, session: SessionType, model: Type[EntryType]) -> None:
        self._session = session
        self.model = model

    @abc.abstractmethod
    async def create(self, **values: Any) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(
            self,
            *clauses: Any,
    ) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
            self,
            *clauses: Any,
            **values: Any
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *clauses: Any) -> Sequence[EntryType]:
        raise NotImplementedError

    async def create_many(
            self,
            data: Sequence[Dict[str, Any]]
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    async def select_many(
            self,
            *clauses: Any,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    async def update_many(self, data: Sequence[Dict[str, Any]]) -> Any:
        raise NotImplementedError

    async def exists(self, *clauses: Any) -> bool:
        raise NotImplementedError

    async def count(self, *clauses: Any) -> int:
        raise NotImplementedError

    async def create_relationship(self, model: Any, **values: Any) -> Any:
        raise NotImplementedError

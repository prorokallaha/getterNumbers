from __future__ import annotations

import abc
from typing import (
    Any,
    Dict,
    Generic,
    Optional,
    Sequence,
    Type,
)

from sqlalchemy import ColumnExpressionArgument

from src.common.types import EntryType, SessionType


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
            *clauses: ColumnExpressionArgument[bool],
    ) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
            self,
            *clauses: ColumnExpressionArgument[bool],
            **values: Any
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *clauses: ColumnExpressionArgument[bool]) -> Sequence[EntryType]:
        raise NotImplementedError

    async def create_many(
            self,
            data: Sequence[Dict[str, Any]]
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    async def select_many(
            self,
            *clauses: ColumnExpressionArgument[bool],
            offset: Optional[int],
            limit: Optional[int],
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    async def update_many(self, data: Sequence[Dict[str, Any]]) -> Any:
        raise NotImplementedError

    async def exists(self, *clauses: ColumnExpressionArgument[bool]) -> bool:
        raise NotImplementedError

    async def count(self, *clauses: ColumnExpressionArgument[bool]) -> int:
        raise NotImplementedError


from __future__ import annotations

import abc
from types import TracebackType
from typing import Generic, Optional, Type, TypeVar

SessionT = TypeVar('SessionT')
TransactionT = TypeVar('TransactionT')


class AbstractUnitOfWork(abc.ABC, Generic[SessionT, TransactionT]):

    def __init__(self, session: SessionT) -> None:
        self._session = session
        self._transaction: Optional[TransactionT] = None

    async def __aenter__(self) -> AbstractUnitOfWork[SessionT, TransactionT]:
        await self._create_transaction()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> None:

        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        await self._close_transaction()

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _create_transaction(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _close_transaction(self) -> None:
        raise NotImplementedError

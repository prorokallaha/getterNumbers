from __future__ import annotations

import abc
from types import TracebackType
from typing import Generic, Optional, Type, TypeVar

SessionType = TypeVar("SessionType")
TransactionType = TypeVar("TransactionType")
Self = TypeVar("Self", bound="TransactionManager")


class TransactionManager(abc.ABC):
    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def __aenter__(self: Self) -> Self:
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_transaction(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def close_transaction(self) -> None:
        raise NotImplementedError


class AbstractTransactionManager(
    TransactionManager, Generic[SessionType, TransactionType]
):
    """
    An abstract base class for implementing the Unit of Work pattern.

    This class provides a generic interface for managing a unit of work
    involving a database session and transactions.

    :param session: The session associated with the unit of work.
    :type session: SessionType
    """

    __slots__ = ("session", "_transaction")

    def __init__(self, session: SessionType) -> None:
        """
        Initialize a new instance of the AbstractUnitOfWork class.

        :param session: The session associated with the unit of work.
        :type session: SessionType
        """
        self.session = session
        self._transaction: Optional[TransactionType] = None

    async def __aenter__(
        self,
    ) -> AbstractTransactionManager[SessionType, TransactionType]:
        await self.create_transaction()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        await self.close_transaction()

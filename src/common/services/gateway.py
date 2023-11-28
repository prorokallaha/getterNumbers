import abc
from typing import Any, TypeVar

from src.common.database.interfaces.unit_of_work import AbstractUnitOfWork
from src.common.types import MediatorType, SessionType, TransactionType

Self = TypeVar('Self', bound='AbstractServiceGateway')


class AbstractServiceGateway(abc.ABC):

    __slots__ = (
        '_uow',
        '_mediator',
    )

    def __init__(
            self,
            unit_of_work: AbstractUnitOfWork[SessionType, TransactionType],
            mediator: MediatorType
    ) -> None:

        self._uow = unit_of_work
        self._mediator = mediator

    async def __aenter__(self: Self) -> Self:
        await self._uow.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._uow.__aexit__(*args)

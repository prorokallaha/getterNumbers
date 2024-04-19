from types import TracebackType
from typing import Optional, Type, TypeVar

from src.database.core.manager import SQlAlchemyTransactionManager
from src.database.repositories import UserRepository

Self = TypeVar("Self", bound="DatabaseGateway")


class DatabaseGateway:
    __slots__ = ("manager",)

    def __init__(self, manager: SQlAlchemyTransactionManager) -> None:
        self.manager = manager

    async def __aenter__(self: Self) -> Self:
        await self.manager.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.manager.__aexit__(exc_type, exc_value, traceback)

    def user(self) -> UserRepository:
        return UserRepository(self.manager.session)


def database_gateway_factory(
    manager: SQlAlchemyTransactionManager,
) -> DatabaseGateway:
    return DatabaseGateway(manager)

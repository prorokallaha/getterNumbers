from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core.gateway import DatabaseGateway, database_gateway_factory
from src.database.core.manager import (
    SQlAlchemyTransactionManager,
    transaction_manager_factory,
)

__all__ = (
    "DatabaseGateway",
    "SQlAlchemyTransactionManager",
    "database_gateway_factory",
    "transaction_manager_factory",
    "transaction_gateway",
    "session_gateway",
)


async def transaction_gateway(session: AsyncSession) -> AsyncIterator[DatabaseGateway]:
    gateway = database_gateway_factory(transaction_manager_factory(session))
    async with gateway:
        yield gateway


async def session_gateway(session: AsyncSession) -> AsyncIterator[DatabaseGateway]:
    gateway = database_gateway_factory(transaction_manager_factory(session))
    async with session:
        yield gateway

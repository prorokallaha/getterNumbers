from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from src.common.interfaces import AbstractTransactionManager
from src.database.exceptions import CommitError, RollbackError


class SQlAlchemyTransactionManager(
    AbstractTransactionManager[AsyncSession, AsyncSessionTransaction]
):
    async def commit(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self.session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err

    async def create_transaction(self) -> None:
        if not self.session.in_transaction() and self.session.is_active:
            self._transaction = await self.session.begin()

    async def close_transaction(self) -> None:
        if self.session.is_active:
            await self.session.close()


def transaction_manager_factory(session: AsyncSession) -> SQlAlchemyTransactionManager:
    return SQlAlchemyTransactionManager(session)

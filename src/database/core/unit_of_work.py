from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from src.database.common.interfaces.unit_of_work import AbstractUnitOfWork
from src.database.exceptions import CommitError, RollbackError


class SQLALchemyUnitOfWork(
    AbstractUnitOfWork[AsyncSession, AsyncSessionTransaction]
):

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err

    async def _create_transaction(self) -> None:
        if self._session.is_active and not self._session.in_transaction():
            self._transaction = await self._session.begin()

    async def _close_transaction(self) -> None:
        await self._session.close()

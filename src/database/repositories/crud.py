from typing import (
    Any,
    Dict,
    Final,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

from sqlalchemy import (
    ColumnExpressionArgument,
    CursorResult,
    TableClause,
    delete,
    exists,
    func,
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database.interfaces import AbstractCRUDRepository
from src.database.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)
ASTERISK: Final[str] = "*"


class SQLAlchemyCRUDRepository(
    AbstractCRUDRepository[AsyncSession, ModelT]
):

    async def create(self, **values: Any) -> Optional[ModelT]:
        stmt = insert(self.model).values(**values).returning(self.model)

        return (await self._session.execute(stmt)).scalars().first()

    async def create_many(self, data: Sequence[Dict[str, Any]]) -> Sequence[ModelT]:
        stmt = insert(self.model).returning(self.model)
        result = await self._session.scalars(stmt, data)
        return result.all()

    async def select(
        self,
        *clauses: ColumnExpressionArgument[bool],
    ) -> Optional[ModelT]:
        stmt = select(self.model).where(*clauses)

        return (await self._session.execute(stmt)).scalars().first()

    async def select_many(
        self,
        *clauses: ColumnExpressionArgument[bool],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[ModelT]:
        stmt = select(self.model).where(*clauses).offset(offset).limit(limit)

        return (await self._session.execute(stmt)).scalars().all()

    async def update(
        self, *clauses: ColumnExpressionArgument[bool], **values: Any
    ) -> Sequence[ModelT]:
        stmt = update(self.model).where(*clauses).values(**values).returning(self.model)

        return (await self._session.execute(stmt)).scalars().all()

    async def update_many(self, data: Sequence[Dict[str, Any]]) -> CursorResult[Any]:
        return await self._session.execute(update(self.model), data)

    async def delete(
        self, *clauses: ColumnExpressionArgument[bool]
    ) -> Sequence[ModelT]:
        stmt = delete(self.model).where(*clauses).returning(self.model)

        return (await self._session.execute(stmt)).scalars().all()

    async def exists(self, *clauses: ColumnExpressionArgument[bool]) -> bool:
        stmt = exists(select(self.model).where(*clauses)).select()
        return cast(bool, await self._session.scalar(stmt))

    async def count(self, *clauses: ColumnExpressionArgument[bool]) -> int:
        stmt = select(func.count(ASTERISK)).where(*clauses).select_from(self.model)

        return cast(int, await self._session.scalar(stmt))

    async def create_relationship(
            self, model: Union[TableClause, Type[Any]], **values: Any
    ) -> None:
        await self._session.execute(insert(model).values(**values))

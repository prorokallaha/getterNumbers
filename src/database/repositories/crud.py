from typing import (
    Any, 
    cast,
    Final,
    Dict, 
    TypeVar,
    Iterable, 
    Optional, 
    Type, 
    Union, 
    Sequence,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    CursorResult, 
    select, 
    insert, 
    update, 
    delete, 
    func,
    exists,
    ColumnExpressionArgument,
)

from src.database.interfaces.repositories.crud import AbstractCRUDRepository
from src.database.models.base import Base


Model = TypeVar('Model', bound=Base)
ASTERISK: Final[str] = '*'


class CRUDRepository(AbstractCRUDRepository[Model]):
    
    def __init__(self, session: AsyncSession, model: Type[Model]) -> None:
        super(CRUDRepository, self).__init__(model)
        self._session = session

    async def create(self, **values: Dict[str, Any]) -> Optional[Model]:

        stmt = (
            insert(self.model)
            .prefix_with('OR IGNORE')
            .values(**values)
            .returning(self.model)
        )
        
        return (await self._session.execute(stmt)).scalars().first() 

    async def create_many(self, data: Iterable[Union[Model, Dict[str, Any]]]) -> Sequence[Model]:

        stmt = (
            insert(self.model)
            .prefix_with('OR IGNORE')
            .returning(self.model)
        )
        params = [model if isinstance(model, dict) else model.as_dict() for model in data]
        result = await self._session.scalars(stmt, params)
        return result.all()
    
    async def select(
            self, 
            *clauses: ColumnExpressionArgument[bool], 
    ) -> Optional[Model]:
        
        stmt = select(self.model).where(*clauses)
        
        return (await self._session.execute(stmt)).scalars().first()
    
    async def select_many(
            self, 
            *clauses: ColumnExpressionArgument[bool], 
            offset: Optional[int] = None, 
            limit: Optional[int] = None, 
    ) -> Sequence[Model]:

        stmt = (
                select(self.model)
                .where(*clauses)
                .offset(offset)
                .limit(limit)
            )
        
        return (await self._session.execute(stmt)).scalars().all()
    
    async def update(self, *clauses: ColumnExpressionArgument[bool], **values: Dict[str, Any]) -> Sequence[Model]:
        
        stmt = (
            update(self.model)
            .where(*clauses)
            .values(**values)
            .returning(self.model)
        )
        
        return (await self._session.execute(stmt)).scalars().all()
    
    async def update_many(self, data: Iterable[Union[Model, Dict[str, Any]]]) -> CursorResult[Any]:

        params = [model if isinstance(model, dict) else model.as_dict() for model in data]
        
        return (await self._session.execute(update(self.model), params))

    async def delete(self, *clauses: ColumnExpressionArgument[bool]) -> Sequence[Model]:
        
        stmt = (
            delete(self.model)
            .where(*clauses)
            .returning(self.model)
        )
        
        return (await self._session.execute(stmt)).scalars().all()
    
    async def exists(
            self, *clauses: ColumnExpressionArgument[bool]
    ) -> bool:
        
        stmt = (
            exists(
                select(self.model)
                .where(*clauses)
            )
            .select()

        )
        return cast(bool, await self._session.scalar(stmt))
    
    async def count(
            self,
            *clauses: ColumnExpressionArgument[bool]
    ) -> int:
        
        stmt = (
            select(func.count(ASTERISK))
            .where(*clauses)
            .select_from(self.model)
        )

        return cast(int, await self._session.scalar(stmt))
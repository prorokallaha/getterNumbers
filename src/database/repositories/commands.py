from typing import Optional, Type, Sequence

from src.common.dto.commands import CommandCreate, CommandUpdate

from src.database.models.commands import Commands
from src.database.repositories.base import BaseRepository


class CommandsRepository(BaseRepository[Commands]):
    __slots__ = ()
    model: Type[Commands] = Commands

    async def select(self, command_tag: str) -> Optional[Commands]:
        return await self._crud.select(self.model.tag == command_tag)

    async def select_many(
            self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Sequence[Commands]:
        return await self._crud.select_many(limit=limit, offset=offset)

    async def exists(self, command_id: int) -> bool:
        return await self._crud.exists(command_id == command_id)

    async def create(self, query: CommandCreate) -> Optional[Commands]:
        return await self._crud.create(**query.dict())

    async def update(
            self, command_id: int, query: CommandUpdate
    ) -> Optional[Commands]:
        result = await self._crud.update(
            self.model.id == command_id, **query.dict(exclude_unset=True)
        )
        return result[0] if result else None

    async def delete(self, command_id: int) -> Optional[Commands]:
        result = await self._crud.delete(command_id == command_id)
        return result[0] if result else None

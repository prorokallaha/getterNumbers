from typing import Optional, Sequence, Type

from src.common.dto.messages import MessagesCreate, MessageUpdate
from src.database.models.messages import Messages
from src.database.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Messages]):
    __slots__ = ()
    model: Type[Messages] = Messages

    async def select(self, message_id: int) -> Optional[Messages]:
        return await self._crud.select(self.model.id == message_id)

    async def select_many(
            self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Sequence[Messages]:
        return await self._crud.select_many(limit=limit, offset=offset)

    async def exists(self, message_id: int) -> bool:
        return await self._crud.exists(self.model.id == message_id)

    async def create(self, query: MessagesCreate) -> Optional[Messages]:
        return await self._crud.create(**query.dict())

    async def update(
            self, message_id: int, query: MessageUpdate
    ) -> Optional[Messages]:
        result = await self._crud.update(
            self.model.id == message_id, **query.dict(exclude_none=True)
        )
        return result[0] if result else None

    async def delete(self, message_id: int) -> Optional[Messages]:
        result = await self._crud.delete(self.model.id == message_id)
        return result[0] if result else None

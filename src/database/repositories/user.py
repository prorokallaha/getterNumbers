from __future__ import annotations

from typing import Optional, Sequence, Type

import src.common.dto as dto
import src.database.models as models
from src.database.models import User
from src.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    __slots__ = ()
    model: Type[User] = User

    async def select(self, user_id: int) -> Optional[models.User]:
        return await self._crud.select(self.model.id == user_id)

    async def select_by_username(self, username: str) -> Optional[models.User]:
        return await self._crud.select(self.model.username == username)

    async def select_many(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Sequence[models.User]:
        return await self._crud.select_many(limit=limit, offset=offset)

    async def exists(self, user_id: int) -> bool:
        return await self._crud.exists(self.model.id == user_id)

    async def create(self, query: dto.UserCreate) -> Optional[models.User]:
        return await self._crud.create(**query.model_dump())

    async def update(
        self, user_id: int, query: dto.UserUpdate
    ) -> Optional[models.User]:
        result = await self._crud.update(
            self.model.id == user_id, **query.model_dump(exclude_none=True)
        )
        return result[0] if result else None

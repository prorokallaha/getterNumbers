from __future__ import annotations

from typing import Optional

import src.common.dto as dto
import src.database.models as models
from src.database.repositories.base import BaseInteractor


class UserWriter(BaseInteractor[models.User]):
    __slots__ = ()

    async def create(self, query: dto.UserCreate) -> Optional[models.User]:
        return await self.repository._crud.create(**query.model_dump())

    async def update(
        self, user_id: int, query: dto.UserUpdate
    ) -> Optional[models.User]:
        result = await self.repository._crud.update(
            self.repository.model.id == user_id, **query.model_dump(exclude_none=True)
        )
        return result[0] if result else None

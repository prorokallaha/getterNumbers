from typing import Optional, Type

from src.common.dto import UserCreate, UserUpdate
from src.database.models.user import User
from src.services.database.services.base import BaseService


class UserService(BaseService[User]):
    model: Type[User] = User

    async def create_user(self, query: UserCreate) -> Optional[User]:
        return await self._crud_repo.create(**query.model_dump(exclude_none=True))

    async def select_user(self, user_id: int) -> Optional[User]:
        return await self._crud_repo.select(self.model.id == user_id)

    async def update_user(
        self, user_id: int, query: UserUpdate, exclude_none: bool = True
    ) -> Optional[User]:
        result = await self._crud_repo.update(
            self.model.id == user_id, **query.model_dump(exclude_none=exclude_none)
        )
        return result[0] if result else None

    async def delete_user(self, user_id: int) -> Optional[User]:
        result = await self._crud_repo.delete(self.model.id == user_id)
        return result[0] if result else None

    async def is_user_exists(self, user_id: int) -> bool:
        return await self._crud_repo.exists(self.model.id == user_id)

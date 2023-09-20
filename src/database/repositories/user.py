from typing import (
    Optional,
    Type,
    List,
    ClassVar,
)

from src.database.repositories.base import BaseRepository
from src.database.models.user import User
from src.database.interfaces.repositories.base import Repository
from src.database.dto import (
    UserCreate, 
    UserDTO,
    UserUpdate,
)
from src.database.converters import convert_user_model_to_dto


class UserRepository(
    BaseRepository[User], 
    Repository[int, UserDTO, UserCreate, UserUpdate]
):

    model: Type[User] = User

    async def create(self, query: UserCreate) -> Optional[UserDTO]:
        result = await self._crud.create(**query.model_dump(exclude_none=True))
        if not result:
            return None
        
        return convert_user_model_to_dto(result)
    
    async def select(self, user_id: int) -> Optional[UserDTO]:
        result = await self._crud.select(self.model.user_id==user_id)
        if not result:
            return None
        
        return convert_user_model_to_dto(result)
    
    async def update(
            self, user_id: int, query: UserUpdate, exclude_none: bool = True
    ) -> List[UserDTO]:
        result = await self._crud.update(
            self.model.user_id==user_id,
            **query.model_dump(exclude_none=exclude_none)
        )
        return [convert_user_model_to_dto(model) for model in result]

    async def delete(self, user_id: int) -> List[UserDTO]:
        result = await self._crud.delete(self.model.user_id==user_id)
        return [convert_user_model_to_dto(model) for model in result]
    
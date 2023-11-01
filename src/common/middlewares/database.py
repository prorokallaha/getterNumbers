from typing import (
    Any, 
    Awaitable, 
    Callable, 
    Dict,
    Optional,
)

from aiogram import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncEngine

from src.database.core.connection import (
    async_engine, 
    create_session_factory, 
    async_session,
)
from src.database.core import Database
from src.database.dto import UserCreate


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, engine: Optional[AsyncEngine] = None) -> None:
        self._session_factory = create_session_factory(engine or async_engine())

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        data['db_pool'] = self._session_factory
        return await handler(event, data)


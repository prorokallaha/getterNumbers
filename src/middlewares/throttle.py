from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Final,
)

from aiogram import BaseMiddleware
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, TelegramObject

TRIGGER_VALUE: Final[int] = 4
DEFAULT_MESSAGE_TIMEOUT: Final[int] = 10
DEFAULT_CALLBACK_TIMEOUT: Final[int] = 1


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(
            self, storage: BaseStorage
    ) -> None:
        self._storage = storage

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        if isinstance(self._storage, MemoryStorage):
            raise ValueError('Throttle middleware working only with RedisStorage instance')

        if isinstance(event, CallbackQuery):
            user = f'user_call_{event.from_user.id}'
            timeout = DEFAULT_CALLBACK_TIMEOUT
            message = 'Эй, эй, палехче'
        if isinstance(event, Message):
            user = f'user_message_{event.from_user.id}' # type: ignore
            timeout = DEFAULT_MESSAGE_TIMEOUT
            message = 'Не нужно торопиться, вводите данные умеренней'

        is_throttled = await self._storage.redis.get(user) # type: ignore
        if is_throttled:
            count = int(is_throttled.decode())
            if count == TRIGGER_VALUE:
                await self._storage.redis.set(name=user, value=count + 1, ex=timeout) # type: ignore
                if isinstance(event, CallbackQuery):
                    return await event.answer(message, show_alert=True)
                return await event.answer(message) # type: ignore
            elif count > TRIGGER_VALUE:
                return
            else:
                await self._storage.redis.set(name=user, value=count + 1, ex=timeout) # type: ignore
        else:
            await self._storage.redis.set(name=user, value=1, ex=timeout) # type: ignore

        if isinstance(event, CallbackQuery):
            await event.answer() # fix loading issue
        return await handler(event, data)

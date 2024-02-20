from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.utils.interactions.chat import ChatFunctionPagination


class ChatMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._chat = ChatFunctionPagination()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["chat"] = self._chat
        data["user"] = event.from_user  # type: ignore
        result = await handler(event, data)
        if result:
            if isinstance(event, CallbackQuery):
                self._chat.set_message(
                    f"{event.from_user.id}:{event.message.chat.id}", result
                )
            if isinstance(event, Message):
                self._chat.set_message(f"{event.from_user.id}:{event.chat.id}", result)

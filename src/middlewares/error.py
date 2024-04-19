from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject

from src.common.logger import Logger
from src.utils.interactions import safe_delete_message


class ErrorMiddleware(BaseMiddleware):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            self._logger.exception(f"{e}")
            await safe_delete_message(event)  # type: ignore
            if isinstance(event, types.CallbackQuery):
                await event.message.answer("Что-то пошло не так, попробуйте еще раз.")
            if isinstance(event, types.Message):
                await event.answer(
                    "Что-то пошло не так, чтобы начать снова введите /start"
                )

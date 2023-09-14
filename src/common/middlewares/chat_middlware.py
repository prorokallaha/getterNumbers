from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram import types
from aiogram.types import TelegramObject

from src.common.middlewares.i18n import gettext as _



class ChatMiddleware(BaseMiddleware):

    def __init__(self) -> None:

        from src.utils.interactions.chat import Chat
        self._chat = Chat()

    async def __call__(
            self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
    ) -> Any:
    
        
        data['chat'] = self._chat
        result = await handler(event, data)
        if isinstance(result, types.Message):
            self._chat.set_message(event.from_user.id, result) # type: ignore
        
        return result
    
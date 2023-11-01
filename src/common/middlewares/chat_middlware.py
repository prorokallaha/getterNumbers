from typing import Any, Awaitable, Callable, Dict
from functools import partial

from aiogram import BaseMiddleware
from aiogram import types
from aiogram.types import TelegramObject

from src.common.middlewares.i18n import gettext as _



class ChatMiddleware(BaseMiddleware):

    def __init__(self) -> None:

        from src.utils.interactions.chat import ChatFunctionPagination
        self._chat = ChatFunctionPagination()

    async def __call__(
            self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
    ) -> Any:
    
        
        data['chat'] = self._chat
        result = await handler(event, data)
        if result:
            pfunc = partial(handler, event, data)
            self._chat.set_message(event.from_user.id, pfunc) # type: ignore
        
        return result
    
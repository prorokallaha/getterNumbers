from typing import Union

from aiogram import types
from aiogram.enums.chat_type import ChatType
from aiogram.filters import Filter


class IsChatType(Filter):
    def __init__(self, chat_type: ChatType) -> None:
        self._chat_type = chat_type

    async def __call__(self, event: Union[types.CallbackQuery, types.Message]) -> bool:
        return event.chat.type == self._chat_type

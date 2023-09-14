from typing import (
    Dict, 
    Any,
    Optional,
    Union,
    List,
)

from pydantic import BaseModel
from aiogram.methods import SendMessage
from aiogram import types

from src.utils.text import START_COMMAND_MESSAGE
from src.utils.buttons import test_button
from src.common.keyboards import build_markup
from src.common.middlewares.i18n import gettext as _


class DefaultMessage(BaseModel):

    text: str = _(START_COMMAND_MESSAGE)
    reply_markup: Union[
        types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup
    ] = build_markup(test_button())


class Chat:

    def __init__(self) -> None:
        self.users: Dict[int, Any] = {}
        
    def get_last_message(
            self, user_id: int
    ) -> Union[types.Message, DefaultMessage]:
        
        last_message: List[Union[types.Message, DefaultMessage]] 
        last_message = self.users.get(user_id, [])

        if len(last_message) <= 1:
            return DefaultMessage()
        
        last_message.pop() 
        return last_message[-1]
      
        
    def set_message(
            self, 
            user_id: int, 
            message: types.Message,
            start_message: bool = False,
            replace_last: bool = False
    ) -> None:
        
        stack = self.users.get(user_id, [])
        if replace_last and stack:
            stack.pop()
        stack.append(message)
        self.users[user_id] = stack if not start_message else [message]
    
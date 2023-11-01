from typing import (
    Dict, 
    Any,
    Optional,
    List,
    Awaitable,
    Union
)

from functools import partial
from aiogram import types

from src.common.middlewares.i18n import gettext as _



class ChatMessagePagination:

    def __init__(self) -> None:
        self.users: Dict[int, Any] = {}
        
    def get_last_message(
            self, 
            user_id: int,
            default_message: Optional[types.Message] = None
    ) -> types.Message:
        
        last_message: List[types.Message] 
        last_message = self.users.get(user_id, [])

        if len(last_message) <= 1:
            return default_message or last_message[-1]
        
        last_message.pop() 
        return last_message[-1]
      
        
    def set_message(
            self, 
            user_id: int, 
            message: types.Message,
            start_message: bool = False,
    ) -> None:
        
        stack = self.users.get(user_id, [])
        stack.append(message)
        self.users[user_id] = stack if not start_message else [message]


class ChatFunctionPagination:

    def __init__(self) -> None:
        self.users: Dict[Union[int, str], Any] = {}
        
    def get_last_message(
            self, 
            user_id: int,
            default_func: Optional[partial[Awaitable[Any]]] = None
    ) -> partial[Awaitable[Any]]:
        
        last_message_func_stack: List[partial[Awaitable[Any]]] 
        last_message_func_stack = self.users.get(user_id, [])

        if len(last_message_func_stack) <= 1:
            return default_func or last_message_func_stack[-1]
        
        last_message_func_stack.pop() 
        return last_message_func_stack[-1]
      
    def set_message(
            self, 
            user_id: int, 
            pfunc: partial[Awaitable[Any]],
            start_message: bool = False,
    ) -> None:
        
        stack = self.users.get(user_id, [])
        stack.append(pfunc)
        self.users[user_id] = stack if not start_message else [pfunc]
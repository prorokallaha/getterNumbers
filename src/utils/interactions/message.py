from functools import wraps
from typing import Any, Callable, Coroutine, Optional, ParamSpec, TypeVar, Union

from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import DeleteMessage
from aiogram.types import CallbackQuery, Message

P = ParamSpec("P")
R = TypeVar("R")


async def safe_delete_message(
    event: Union[CallbackQuery, Message],
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
) -> Union[DeleteMessage, bool]:
    try:
        if all([chat_id, message_id]):
            msg = await event.bot.delete_message(
                chat_id=chat_id,  # type: ignore
                message_id=message_id,  # type: ignore
            )
        else:
            if isinstance(event, Message):
                msg = await event.delete()
            else:
                msg = await event.message.delete()
    except TelegramBadRequest:
        return False

    return msg


async def safe_edit_message(
    event: Union[CallbackQuery, Message],
    text: str,
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    **kwargs: Any,
) -> Union[Message, bool]:
    try:
        if all([chat_id, message_id]):
            msg = await event.bot.edit_message_text(
                text=text, chat_id=chat_id, message_id=message_id, **kwargs
            )
        else:
            if isinstance(event, Message):
                msg = await event.edit_text(text=text, **kwargs)
            else:
                msg = await event.message.edit_text(text=text, **kwargs)
    except TelegramBadRequest:
        return False

    return msg


def on_loading(
    coro: Callable[P, Coroutine[None, None, R]],
) -> Callable[P, Coroutine[None, None, R]]:
    @wraps(coro)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        update = kwargs.get("event_update")
        if not hasattr(update, "callback_query"):
            raise TypeError("`on_loading` should be using only with callbacks")

        callback = update.callback_query

        await safe_edit_message(callback, "loading...")
        return await coro(*args, **kwargs)

    return _wrapper

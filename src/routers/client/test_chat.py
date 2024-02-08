from typing import Any

from aiogram import F, Router, types

from src.keyboards import build_markup, button
from src.keyboards.buttons import (
    back_button,
)
from src.utils.interactions import (
    BackButtonReturnType,
    safe_edit_message,
)


def register_test_chat(router: Router) -> None:
    router.callback_query.register(inner_chat_callback, F.data == "inner_chat_test")
    router.callback_query.register(inner_chat_2_callback, F.data == "inner_chat_test_2")
    router.callback_query.register(inner_chat_3_callback, F.data == "inner_chat_test_3")
    router.callback_query.register(inner_chat_4_callback, F.data == "inner_chat_test_4")


async def inner_chat_callback(
    call: types.CallbackQuery, **_: Any
) -> BackButtonReturnType:
    await safe_edit_message(
        call,
        "This is inner chat 1",
        reply_markup=build_markup(
            [
                button(text="Inner Chat 2", callback_data="inner_chat_test_2"),
                back_button(),
            ]
        ),
    )
    return inner_chat_callback


async def inner_chat_2_callback(
    call: types.CallbackQuery, **_: Any
) -> BackButtonReturnType:
    await safe_edit_message(
        call,
        "This is inner chat 2",
        reply_markup=build_markup(
            [
                button(text="Inner Chat 3", callback_data="inner_chat_test_3"),
                back_button(),
            ]
        ),
    )
    return inner_chat_2_callback


async def inner_chat_3_callback(
    call: types.CallbackQuery, **_: Any
) -> BackButtonReturnType:
    await safe_edit_message(
        call,
        "This is inner chat 3",
        reply_markup=build_markup(
            [
                button(text="Inner Chat 4", callback_data="inner_chat_test_4"),
                back_button(),
            ]
        ),
    )
    return inner_chat_3_callback


async def inner_chat_4_callback(
    call: types.CallbackQuery, **_: Any
) -> BackButtonReturnType:
    await safe_edit_message(
        call, "This is inner chat 4", reply_markup=build_markup([back_button()])
    )
    return inner_chat_4_callback

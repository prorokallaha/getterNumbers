from typing import Any

from aiogram import F, types

from src.keyboards import build_markup
from src.keyboards.buttons import (
    back_button,
)
from src.routers.client.router import client_router
from src.utils.interactions import (
    BackButtonReturnType,
    safe_edit_message,
)


@client_router.callback_query(F.data == 'inner_chat_test')
async def inner_chat_callback(
    call: types.CallbackQuery,
    **kwargs: Any
) -> BackButtonReturnType:

    await safe_edit_message(
        call,
        'This is inner chat 1',
        reply_markup=build_markup(
            [
                {'text': 'Inner Chat 2', 'callback_data': 'inner_chat_test_2'},
                back_button()
            ]
        )
    )
    return inner_chat_callback


@client_router.callback_query(F.data == 'inner_chat_test_2')
async def inner_chat_2_callback(
    call: types.CallbackQuery,
    **kwargs: Any
) -> BackButtonReturnType:

    await safe_edit_message(
        call,
        'This is inner chat 2',
        reply_markup=build_markup(
            [
                {'text': 'Inner Chat 3', 'callback_data': 'inner_chat_test_3'},
                back_button()
            ]
        )
    )
    return inner_chat_2_callback


@client_router.callback_query(F.data == 'inner_chat_test_3')
async def inner_chat_3_callback(
    call: types.CallbackQuery,
    **kwargs: Any
) -> BackButtonReturnType:

    await safe_edit_message(
        call,
        'This is inner chat 3',
        reply_markup=build_markup(
            [
                {'text': 'Inner Chat 4', 'callback_data': 'inner_chat_test_4'},
                back_button()
            ]
        )
    )
    return inner_chat_3_callback


@client_router.callback_query(F.data == 'inner_chat_test_4')
async def inner_chat_4_callback(
    call: types.CallbackQuery,
    **kwargs: Any
) -> BackButtonReturnType:

    await safe_edit_message(
        call,
        'This is inner chat 4',
        reply_markup=build_markup(
            [
                back_button()
            ]
        )
    )
    return inner_chat_4_callback

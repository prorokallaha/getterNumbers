from typing import Union

from aiogram import types, F

from src.routers.client.router import client_router
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.common.keyboards.buttons import (
    back_button,
)
from src.utils.interactions import (
    safe_edit_message,
)


@client_router.callback_query(F.data == 'inner_chat_test')
async def inner_chat_callback(
    call: types.CallbackQuery,
) -> Union[types.Message, bool]:
    
    msg = await safe_edit_message(
        call,
        'This is inner chat 1',
        reply_markup=build_markup(
            [
                {'text': 'Inner Chat 2', 'callback_data': 'inner_chat_test_2'},
                back_button()
            ]
        )
    )
    return msg


@client_router.callback_query(F.data == 'inner_chat_test_2')
async def inner_chat_2_callback(
    call: types.CallbackQuery,
) -> Union[types.Message, bool]:
    
    msg = await safe_edit_message(
        call,
        'This is inner chat 2',
        reply_markup=build_markup(
            [
                {'text': 'Inner Chat 3', 'callback_data': 'inner_chat_test_3'},
                back_button()
            ]
        )
    )
    return msg


@client_router.callback_query(F.data == 'inner_chat_test_3')
async def inner_chat_3_callback(
    call: types.CallbackQuery,
) -> Union[types.Message, bool]:
    
    msg = await safe_edit_message(
        call,
        'This is inner chat 3',
        reply_markup=build_markup(
            [
                {'text': 'Inner Chat 4', 'callback_data': 'inner_chat_test_4'},
                back_button()
            ]
        )
    )
    return msg


@client_router.callback_query(F.data == 'inner_chat_test_4')
async def inner_chat_4_callback(
    call: types.CallbackQuery,
) -> Union[types.Message, bool]:
    
    msg = await safe_edit_message(
        call,
        'This is inner chat 4',
        reply_markup=build_markup(
            [
                back_button()
            ]
        )
    )
    return msg
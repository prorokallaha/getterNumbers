from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import types, F

from src.routers.client.router import client_router
from src.utils.text import TEST_PAGINATION_MESSAGE
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.utils.buttons import (
    pagination_data_button, 
    next_pagination_button, 
    previous_pagination_button,
    back_button,
)
from src.utils.interactions import (
    PaginationMediator,
    Chat, 
    safe_delete_message,
    safe_edit_message,
)



@client_router.callback_query(F.data == 'inner_chat_test')
async def inner_chat_callback(
    call: types.CallbackQuery,
    chat: Chat
) -> types.Message:
    
    await safe_delete_message(call)
    msg = await call.message.answer(
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
    chat: Chat
) -> types.Message:
    
    await safe_delete_message(call)
    msg = await call.message.answer(
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
    chat: Chat
) -> types.Message:
    
    await safe_delete_message(call)
    msg = await call.message.answer(
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
    chat: Chat
) -> types.Message:
    
    await safe_delete_message(call)
    msg = await call.message.answer(
        'This is inner chat 4',
        reply_markup=build_markup(
            [
                back_button()
            ]
        )
    )
    return msg
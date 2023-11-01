from functools import partial

from aiogram.fsm.context import FSMContext
from aiogram import types, F
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.routers.client.router import client_router
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.common.keyboards.buttons import (
    next_pagination_button, 
    previous_pagination_button,
    back_button,
)
from src.utils.interactions import (
    DataPaginationMediator,
    ChatFunctionPagination, 
    safe_edit_message,
)

from src.routers.client.commands.test_start import start


@client_router.callback_query(F.data == 'back')
async def back_callback(
    call: types.CallbackQuery, 
    chat: ChatFunctionPagination,
    pagination: DataPaginationMediator,
    state: FSMContext,
    db_pool: async_sessionmaker[AsyncSession]
) -> None:
    
    data = (await state.get_data()).get('pagination')
    
    if data and data.get('flag'):
        try:
            await safe_edit_message(
                call,
                text=data.get('text'),
                reply_markup=build_markup(data.get('reply_markup'))
            )
        except TypeError:
            await state.update_data(pagination={})
            return await back_callback(call, chat, pagination, state, db_pool) # type: ignore
    else:
        default_message = partial(start, call.message, chat, pagination, db_pool)
        last_message = chat.get_last_message(call.from_user.id, default_message)
        if last_message.func.__name__ == 'start':
            await call.message.delete()
        pagination.clear(call.from_user.id)
        await last_message()
    await state.update_data(pagination={})
    await state.set_state()


@client_router.callback_query(F.data == 'next')
async def next_data_callback(
    call: types.CallbackQuery, pagination: DataPaginationMediator, state: FSMContext
) -> None:
    
    data = pagination.get(call.from_user.id)
    buttons = [data.func((str(i), str(i))) for i in data.next()]
    buttons += [previous_pagination_button()]
    if data.is_next_data_exists():
        buttons += [next_pagination_button()]
    buttons += [back_button()]
    await safe_edit_message(
        call,
        text=data.text,
        reply_markup=build_markup(buttons)
    )
    await state.update_data(pagination={'text': data.text, 'reply_markup': buttons, 'flag': False})
    

@client_router.callback_query(F.data == 'previous')
async def previous_data_callback(
    call: types.CallbackQuery, pagination: DataPaginationMediator, state: FSMContext
) -> None:
    
    data = pagination.get(call.from_user.id)
    buttons = [data.func((str(i), str(i))) for i in data.previous()]
    if data.is_previous_data_exists():
        buttons += [previous_pagination_button()]
        buttons += [next_pagination_button(), back_button()]
    else:
        buttons += [back_button(), next_pagination_button()]
    await safe_edit_message(
        call,
        text=data.text,
        reply_markup=build_markup(buttons)
    )
    await state.update_data(pagination={'text': data.text, 'reply_markup': buttons, 'flag': False})

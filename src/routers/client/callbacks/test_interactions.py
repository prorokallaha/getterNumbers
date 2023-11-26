from typing import Any

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.keyboards import build_markup
from src.keyboards.buttons import (
    back_button,
    next_pagination_button,
    previous_pagination_button,
)
from src.routers.client.commands.test_start import start_message
from src.routers.client.router import client_router
from src.utils.interactions import (
    ChatFunctionPagination,
    DatabaseDataPaginationMediator,
    safe_delete_message,
    safe_edit_message,
)


@client_router.callback_query(F.data == "back")
async def back_callback(
        call: types.CallbackQuery,
        chat: ChatFunctionPagination,
        pagination: DatabaseDataPaginationMediator,
        state: FSMContext,
        db_pool: async_sessionmaker[AsyncSession],
        **kwargs: Any
) -> None:

    last_message = chat.get_last_message(call.from_user.id)
    if not last_message:
        await safe_delete_message(call)
        await start_message(
            call.message,
            chat=chat,
            state=state,
            pagination=pagination,
            db_pool=db_pool,
            **kwargs
        )
    else:
        func_name = last_message.__name__
        if func_name.endswith('message'):
            if func_name == 'start_message':
                await safe_delete_message(call)
            await last_message(
                call.message,
                chat=chat,
                state=state,
                pagination=pagination,
                db_pool=db_pool,
                **kwargs
            )
        if func_name.endswith('callback'):
            await last_message(
                call,
                chat=chat,
                state=state,
                pagination=pagination,
                db_pool=db_pool,
                **kwargs
            )
    await state.set_state()


@client_router.callback_query(F.data == "next")
async def next_data_callback(
        call: types.CallbackQuery,
        pagination: DatabaseDataPaginationMediator
) -> None:

    data = pagination.get(call.from_user.id)

    buttons = [data.dfunc(elem) for elem in await data.next()]
    buttons += [previous_pagination_button()]
    if await data.is_next_data_exists():
        buttons += [next_pagination_button()]
    buttons += [back_button()]

    await safe_edit_message(call, text=data.text, reply_markup=build_markup(buttons))


@client_router.callback_query(F.data == "previous")
async def previous_data_callback(
        call: types.CallbackQuery,
        pagination: DatabaseDataPaginationMediator
) -> None:

    data = pagination.get(call.from_user.id)

    buttons = [data.dfunc(elem) for elem in await data.previous()]
    if await data.is_previous_data_exists():
        buttons += [previous_pagination_button()]
        buttons += [next_pagination_button(), back_button()]
    else:
        buttons += [back_button(), next_pagination_button()]

    await safe_edit_message(call, text=data.text, reply_markup=build_markup(buttons))

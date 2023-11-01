from typing import Union

from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.routers.client.router import client_router
from src.utils.text import TEST_PAGINATION_MESSAGE
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.common.keyboards.buttons import (
    pagination_data_button, 
    next_pagination_button, 
    back_button,
)
from src.utils.interactions import (
    DataPaginationMediator,
    safe_edit_message,
)


@client_router.callback_query(F.data == 'test')
async def test_button(
    call: types.CallbackQuery, pagination: DataPaginationMediator, state: FSMContext
) -> bool:
    
    pagination.add(call.from_user.id, list(range(100)), _(TEST_PAGINATION_MESSAGE), pagination_data_button)
    data = pagination.get(call.from_user.id)
    buttons = [pagination_data_button((str(i), str(i))) for i in data.next()]
    if buttons:
        buttons += [back_button(), next_pagination_button()]
    else:
        buttons += [back_button()]
    await safe_edit_message(
        call,
        data.text,
        reply_markup=build_markup(buttons)
    )
    await state.update_data(pagination={'text': data.text, 'reply_markup': buttons})
    return True

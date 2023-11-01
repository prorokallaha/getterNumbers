from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.routers.client.router import client_router
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.common.keyboards.buttons import (
    back_button,
)
from src.utils.interactions import (
    safe_delete_message,
)



@client_router.callback_query(F.data.regexp(r'data:.+'))
async def inner_data_callback(
    call: types.CallbackQuery, state: FSMContext
) -> None:

    await safe_delete_message(call)
    data = call.data.split(':')[-1]
    await call.message.answer(
        text=_(f'Your number of test-data: {data}. Deal with it'),
        reply_markup=build_markup(back_button())
    )
    pagination = (await state.get_data()).get('pagination', {})
    pagination['flag'] = True
    await state.update_data(pagination=pagination)
    
    
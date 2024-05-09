from typing import Any

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.common.logger import Logger
from src.filters.admin import IsAdmin
from src.keyboards import default_keyboard
from src.keyboards.buttons.admin import (
    add_commands,
    update_commands,
    delete_commands,
    history_messages,
    select_users,
    cancel_button
)


def register_start(router: Router) -> None:
    router.message.register(start_message, CommandStart(), IsAdmin())
    router.message.register(cancel_message, F.text.lower()== "отмена")


async def start_message(
        message: types.Message,
        user: types.User,
        state: FSMContext,
        logger: Logger,
        **_: Any,
) -> None:
    logger.debug(f"Admin {user.username or user.id} is start_message menu")
    keyboard = default_keyboard(
        reply_keyboard=[
            [add_commands(), delete_commands()],
            [update_commands(), select_users()],
            [cancel_button()],
        ], resize_keyboard=True,
    )
    await message.answer("Привет админ. Что ты хочещь сделать?", reply_markup=keyboard)
    await state.set_state()


async def cancel_message(
        message: types.Message,
        user: types.User,
        state: FSMContext,
        logger: Logger
) -> None:
    await start_message(message=message, user=user, state=state, logger=logger)
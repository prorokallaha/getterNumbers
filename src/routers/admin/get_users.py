from typing import Any, Annotated

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.common.logger import Logger
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.database import DatabaseGateway
from src.filters.admin import IsAdmin
from src.keyboards import default_keyboard


def register_user(router: Router) -> None:
    router.message.register(handle_get_users, F.text.lower() == "показать пользователей")


async def handle_get_users(
        message: types.Message,
        state: FSMContext,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    await display_users(message, state)


@inject
async def display_users(
        message: types.Message,
        state: FSMContext,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    users_repository = gateway.user()
    users = await users_repository.select_many(limit=2)
    keyboard = InlineKeyboardBuilder()
    if users:
        for user in users:
            callback_data = f"user_{user.id}"
            keyboard.add(InlineKeyboardButton(text=user.username, callback_data=callback_data))
        keyboard = keyboard.adjust(5).as_markup()
        await message.answer("Список последних пользователей:", reply_markup=keyboard)
    else:
        await message.answer("Нет пользователей для отображения.")

    await state.set_state()


def register_callback(router: Router) -> None:
    router.callback_query.register(user_callback, F.data.startswith("user_"))


@inject
async def user_callback(
        query: types.CallbackQuery,
        state: FSMContext,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    user_repository = gateway.user()
    user_id = int(query.data.split("_")[1])
    user_info = await user_repository.select(user_id=user_id)
    await query.message.answer(f"Info about {user_info.username}:\nnumber: {user_info.number}\nid: {user_info.id}")
    await query.answer()

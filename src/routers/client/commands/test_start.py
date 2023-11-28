from typing import Any

from aiogram import types
from aiogram.filters.command import CommandStart

from src.common.dto import UserCreate
from src.keyboards import build_markup
from src.keyboards.buttons import test_button
from src.routers.client.router import client_router
from src.services.database import ServiceGateway
from src.utils.decorators import with_database_service
from src.utils.interactions import ChatFunctionPagination, DataPaginationMediator


@client_router.message(CommandStart(ignore_mention=True))
@with_database_service  # if you want to use db moments in specific handler
async def start_message(
    message: types.Message,
    chat: ChatFunctionPagination,
    pagination: DataPaginationMediator,
    user: types.User,
    service: ServiceGateway,
    **kwargs: Any
) -> None:
    await message.answer(text="First message", reply_markup=build_markup(test_button()))
    user_id = user.id
    db_user = await service.user.is_user_exists(user_id)
    if not db_user:
        await service.user.create_user(
            UserCreate(**user.model_dump())
        )  # creating a user at start if not exists
    pagination.clear(user_id)
    chat.set_message(user_id, start_message, True)

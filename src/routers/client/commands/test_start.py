from functools import partial

from aiogram.filters.command import Command
from aiogram import types
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.routers.client.router import client_router
from src.common.keyboards.buttons import test_button
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.utils.interactions import ChatFunctionPagination, DataPaginationMediator
from src.utils.text import START_COMMAND_MESSAGE
from src.database.core.database import Database
from src.database.dto import UserCreate


@client_router.message(Command(commands=('start',), ignore_mention=True))
async def start(
    message: types.Message, 
    chat: ChatFunctionPagination,
    pagination: DataPaginationMediator,
    db_pool: async_sessionmaker[AsyncSession],
) -> None:
    
    default_message = partial(start, message, chat, pagination, db_pool)
    await message.answer(
        text=_(START_COMMAND_MESSAGE), 
        reply_markup=build_markup(test_button())
    )
    user_id = message.from_user.id
    user = message.from_user
    async with Database(db_pool()) as db:
        db_user = await db.user.select(user_id)
        if not db_user:
            await db.user.create(UserCreate(
                user_id=user_id,
                **user.model_dump(exclude_none=True, exclude=set('id',))
            ))
    pagination.clear(message.from_user.id)
    chat.set_message(message.from_user.id, default_message, True)

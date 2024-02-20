from typing import Annotated, Any

from aiogram import Router, types
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.common.dto import UserCreate, UserUpdate
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.database import DatabaseGateway
from src.filters import IsChatType
from src.keyboards import build_markup, button
from src.utils.interactions import (
    BackButtonReturnType,
    DatabaseDataPaginationMediator,
)
from src.utils.logger import Logger


def register_start(router: Router) -> None:
    router.message.register(start_message, CommandStart(), IsChatType(ChatType.PRIVATE))


@inject  # whenever you want to use Depends, you should wrap it
async def start_message(  # should be endswith _message if we want to use chat_stack or _callback for callbacks
    message: types.Message,
    user: types.User,
    gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
    pagination: DatabaseDataPaginationMediator,
    state: FSMContext,
    logger: Logger,
    **_: Any,  # this is important thing everywhere to chat capability
) -> BackButtonReturnType:
    logger.debug(f"User {user.username or user.id} in start_message menu")
    repository = gateway.user()
    is_user_exists = await repository.reader().exists(user.id)
    # for i in range(1, 100):
    #     await repository.writer().create(UserCreate(id=i, is_bot=False, first_name='123')) # just once creating for check db pagination
    if not is_user_exists:
        await repository.writer().create(
            UserCreate(**user.model_dump())
        )  # creating a user and put him to db if not exists
    else:
        await repository.writer().update(
            user_id=user.id, query=UserUpdate(**user.model_dump(exclude={"id"}))
        )  # or updating it instead
    await message.answer(
        "Test",
        reply_markup=build_markup(
            [
                button(
                    text="Test inner chat", callback_data="inner_chat_test"
                ),  # test inner chat (aka ChatFunctionPagination)
                button(
                    text="Test pagination", callback_data="paginate_users"
                ),  # test db pagination (aka DatabaseDataPaginationMediator)
            ]
        ),
    )
    pagination.clear(user.id)
    await state.set_state()  # Reset all states if user send /start command
    return start_message

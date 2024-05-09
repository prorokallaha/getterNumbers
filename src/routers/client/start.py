from typing import Annotated, Any

from aiogram import Router, types, F
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InputFile

from src.routers.client.code_request import inline_code_request
from src.common.dto import UserCreate, UserUpdate, MessagesCreate
from src.common.logger import Logger
from src.routers.client.state import CodeRequest
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.database import DatabaseGateway
from src.filters import IsChatType
from src.utils.interactions import (
    ChatFunctionPagination,
    DatabaseDataPaginationMediator,
)

# Инициализация Router
start_router = Router()


@start_router.message(CommandStart(), IsChatType(ChatType.PRIVATE))
@inject
async def start_message(
        message: types.Message,
        user: types.User,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
        pagination: DatabaseDataPaginationMediator,
        state: FSMContext,
        logger: Logger,
        **_: Any,
) -> None:
    logger.debug(f"User {user.username or user.id} in start_message menu")

    user_repository = gateway.user()
    is_user_exists = await user_repository.exists(user.id)
    if not is_user_exists:
        await user_repository.create(UserCreate(**user.model_dump()))
    else:
        await user_repository.update(user_id=user.id, query=UserUpdate(**user.model_dump(exclude={"id"})))

    commands_repository = gateway.commands()
    command_response = await commands_repository.select(command_tag="/start")
    response_text = command_response.text if command_response else f"Привет, {user.username or user.first_name}"
    keyboard = get_contact_keyboard()

    if command_response and command_response.image_item_id:
        await message.answer_photo(photo=command_response.image_item_id, caption=response_text, reply_markup=keyboard,
                                   allow_sending_without_reply=False)
        logger.debug(f"Client: Add photo to message, my message: {command_response.image_item_id}")
    else:
        logger.error(f"File not found: {command_response.image_item_id}")
        await message.answer(text=response_text)

    pagination.clear(user.id)
    await state.set_state(state=CodeRequest.get_number)


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    contact_button = KeyboardButton(text="Поделиться номером телефона", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[contact_button]])
    return keyboard

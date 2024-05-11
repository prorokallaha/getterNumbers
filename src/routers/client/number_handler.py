from typing import Annotated, Any

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.enums.chat_type import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.magic_data import MagicFilter

from src.common.dto import UserCreate, UserUpdate, MessagesCreate
from src.common.logger import Logger
from src.routers.client.state import CodeRequest
from src.routers.client.code_request import inline_code_request
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.routers.client.code_request import get_settings
from src.database import DatabaseGateway
from src.filters import IsChatType
from src.utils.interactions import (
    ChatFunctionPagination,
    DatabaseDataPaginationMediator,
)

number_router = Router()


@number_router.message(StateFilter(CodeRequest.get_number))
@inject
async def handle_contact(
        message: types.Message,
        user: types.User,
        settings: get_settings,
        state: FSMContext,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
        logger: Logger,
        **kwargs,
):
    contact = message.contact
    logger.debug(f"Получен контакт: {contact.phone_number}")

    user_repository = gateway.user()
    await user_repository.update(
        user_id=message.from_user.id,
        query=UserUpdate(number=contact.phone_number)
    )

    text = f"Юзер: {message.from_user.username or message.from_user.first_name}\nНомер телефона: {contact.phone_number}\nОтправил контакт"

    await message.bot.send_message(settings.bot.admins[0], text=text)

    command_repository = gateway.commands()
    keyboard = await inline_code_request()
    command_response = await command_repository.select(command_tag="answer_contact")
    if command_response:
        response_text = command_response.text if command_response.text else "Спасибо за предоставленный контакт"
        if command_response.image_item_id:
            try:
                await message.answer_photo(photo=command_response.image_item_id, caption=response_text, reply_markup=keyboard)
                logger.debug(f"Image sent successfully: {command_response.image_item_id}")
            except Exception as e:
                logger.error(f"Error sending image: {str(e)}")
                await message.answer(text=response_text, reply_markup=keyboard)  # Fallback to text only if image can't be sent
        else:
            await message.answer(text=response_text, reply_markup=keyboard)
    else:
        logger.error("Command response is None, falling back to default message.")
        await message.answer(text="Спасибо за предоставленный контакт", reply_markup=keyboard)

    await state.set_state()

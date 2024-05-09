from typing import Annotated

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from src.common.logger import Logger
from src.common.markers import TransactionGatewayMarker
from src.common.sdi import Depends, inject
from src.database.repositories import message
from src.routers.admin.state import CommandCreation, CommandRemove
from src.database import DatabaseGateway
from src.common.dto import CommandCreate, CommandUpdate
from src.utils.interactions import (
    ChatFunctionPagination,
    DatabaseDataPaginationMediator,
    safe_edit_message
)
from src.keyboards import build_markup
from src.keyboards.buttons import back_button, next_pagination_button, previous_pagination_button


def register_remove_commands(router: Router) -> None:
    router.message.register(handle_remove_comand, F.text.lower() == "удалить команду")
    router.message.register(handle_tag_remove, StateFilter(CommandRemove.waiting_for_tag))


async def handle_remove_comand(message: types.Message, state: FSMContext, logger: Logger) -> None:
    logger.debug("Admin: Удаление команды")
    await message.answer('Напиши тег для команды которую хочешь удалить ("start" = "/start")')
    await state.set_state(CommandRemove.waiting_for_tag)


@inject
async def handle_tag_remove(
        message: types.Message,
        state: FSMContext,
        gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
        logger: Logger) -> None:
    tag = message.text
    if tag == "start":
        tag = "/start"

    logger.debug(f"Admin: Тег получен, удаляем команду {tag}")
    commands_repository = gateway.commands()
    command = await commands_repository.select(command_tag=tag)
    await commands_repository.delete(command_id=command.id)
    await message.answer(f'Команда {tag} - удалена')
    await state.set_state()

# def register_pagination_handlers(
#         router: Router,
#         gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
#         pagination: DatabaseDataPaginationMediator
# ) -> None:
#     repository = gateway.commands()
#     router.callback_query.register(
#         lambda call: display_commands_page(call, pagination, repository, pagination.get(call.from_user.id).page + 1),
#         F.data == "next"
#     )
#     router.callback_query.register(
#         lambda call: display_commands_page(call, pagination, repository,
#                                            max(0, pagination.get(call.from_user.id).page - 1)),
#         F.data == "previous"
#     )
#     router.callback_query.register(
#         lambda call: display_commands_page(call, pagination, repository, 0),
#         F.data == "back"
#     )
#
#
# async def display_commands_page(
#         call: types.CallbackQuery,
#         pagination: DatabaseDataPaginationMediator,
#         repository,
#         page: int = 0
# ) -> None:
#     page_size = 5  # Number of items per page
#     offset = page * page_size
#
#     commands = await repository.select_many(limit=page_size, offset=offset)
#
#     message_text = "\n".join(f"{command.id}: {command.tag} - {command.text}" for command in commands)
#
#     buttons = []
#     if page > 0:
#         buttons.append(previous_pagination_button())
#     if len(commands) == page_size:  # Assume there might be another page
#         buttons.append(next_pagination_button())
#     buttons.append(back_button())
#
#     # Send or edit message
#     await safe_edit_message(call, text=message_text, reply_markup=build_markup(buttons))
#
#     # Add current page to pagination mediator
#     pagination.add(call.from_user.id, lambda elem: elem, repository.select_many, "Commands Page", page)

from typing import Annotated, Any, Dict, Sequence

from aiogram import F, types

import src.database.models as models
from src.common.markers import SessionGatewayMarker
from src.common.sdi import Depends, inject
from src.database import DatabaseGateway
from src.keyboards import build_markup, button
from src.keyboards.buttons import (
    back_button,
    next_pagination_button,
    previous_pagination_button,
)
from src.routers.client.router import client_router
from src.utils.interactions import (
    BackButtonReturnType,
    DatabaseDataPaginationMediator,
    safe_edit_message,
)


def paginated_user_button(user: models.User) -> Dict[str, Any]:
    return button(
        text=f"{user.username or user.id}", callback_data=f"paginated_user:{user.id}"
    )


@client_router.callback_query(F.data == "paginate_users")
async def paginate_users_callback(
    call: types.CallbackQuery, pagination: DatabaseDataPaginationMediator, **_: Any
) -> BackButtonReturnType:
    data = pagination.get(call.from_user.id)
    if data:
        page = data.current_page - 1
    else:
        page = 0

    @inject
    async def paginate(
        offset: int,
        limit: int,
        gateway: Annotated[DatabaseGateway, Depends(SessionGatewayMarker)],
    ) -> Sequence[models.User]:
        return await gateway.user().reader().select_many(limit=limit, offset=offset)

    data = pagination.add(
        call.from_user.id,
        paginated_user_button,
        paginate,
        "Users",
        page,
    )
    if not await data.is_next_data_exists():
        data._page = 0

    buttons = [paginated_user_button(user) for user in await data.next()]
    if buttons:
        if await data.is_previous_data_exists():
            buttons += [previous_pagination_button()]
        if await data.is_next_data_exists():
            buttons += [next_pagination_button()]
        buttons += [back_button()]
    else:
        buttons += [back_button()]
    await safe_edit_message(call, "Users", reply_markup=build_markup(buttons))

    return paginate_users_callback


@client_router.callback_query(F.data.regexp(r"paginated_user:+"))
@inject
async def paginated_user_callback(
    call: types.CallbackQuery,
    gateway: Annotated[DatabaseGateway, Depends(SessionGatewayMarker)],
    **_: Any,
) -> BackButtonReturnType:
    user_id = int(call.data.split(":")[-1])
    user = await gateway.user().reader().select(user_id)
    await safe_edit_message(
        call,
        text=f"ID: {user.id}\nUsername: {user.username}\nIsBot: {user.is_bot}\nHasPremium{user.is_premium}",
        reply_markup=build_markup(back_button()),
    )
    return paginated_user_callback

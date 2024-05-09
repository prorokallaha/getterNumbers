from typing import Optional

from aiogram import Router

from src.routers.admin.start import register_start
from src.routers.admin.commands.create_commands import register_create_commands
from src.routers.admin.commands.remove_change_commands import register_remove_commands
from src.routers.admin.get_users import register_user, register_callback


def register_admin_router(router: Optional[Router] = None) -> Router:
    if router is None:
        router = Router(name="admin")

        register_start(router)
        register_create_commands(router)
        register_remove_commands(router)
        register_callback(router)
        register_user(router)

    return router

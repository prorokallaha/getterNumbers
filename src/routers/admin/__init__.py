from typing import Optional

from aiogram import Router


def register_admin_router(router: Optional[Router] = None) -> Router:
    if router is None:
        router = Router(name="admin")

    return router

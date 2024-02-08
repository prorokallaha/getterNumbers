from typing import Optional

from aiogram import Router

from src.routers.client.interactions import register_interactions
from src.routers.client.start import register_start
from src.routers.client.test_chat import register_test_chat
from src.routers.client.test_db_user_pagination import register_test_pagination


def register_client_router(router: Optional[Router] = None) -> Router:
    if router is None:
        router = Router(name="client")

    # callbacks
    register_interactions(router)

    # NOTE: test
    register_test_chat(router)
    register_test_pagination(router)
    # NOTE: test

    # messages
    register_start(router)

    return router

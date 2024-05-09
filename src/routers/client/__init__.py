from typing import Optional

from aiogram import Router

from src.routers.client.start import start_router
from src.routers.client.code_request import code_router
from src.routers.client.number_handler import number_router


def register_client_router(router: Optional[Router] = None) -> Router:
    if router is None:
        router = Router(name="client")

    router.include_router(start_router)
    router.include_router(number_router)
    router.include_router(code_router)

    return router

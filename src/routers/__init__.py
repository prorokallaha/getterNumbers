from aiogram import Router

from src.routers.client import client_router

router = Router(name='main')
router.include_routers(
    client_router,
)

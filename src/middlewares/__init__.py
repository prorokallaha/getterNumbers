from aiogram import BaseMiddleware, Router

from src.middlewares.chat import ChatMiddleware
from src.middlewares.error import ErrorMiddleware
from src.middlewares.throttle import ThrottlingMiddleware

__all__ = (
    "ThrottlingMiddleware",
    "ErrorMiddleware",
    "ChatMiddleware",
)


def register_middlewares(
    router: Router, *middlewares: BaseMiddleware, is_outer: bool
) -> None:
    for middleware in middlewares:
        if is_outer:
            router.message.outer_middleware.register(middleware)
            router.callback_query.outer_middleware.register(middleware)
        else:
            router.message.middleware.register(middleware)
            router.callback_query.middleware.register(middleware)

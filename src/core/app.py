from __future__ import annotations

from typing import Any, Optional, TypedDict

from aiogram import (
    BaseMiddleware,
    Bot,
    Dispatcher,
    Router,
)
from aiogram.types import BotCommand

from src.core.settings import Settings


class CommandType(TypedDict):
    command: str
    description: str


class BotApplication:

    def __init__(
            self,
            settings: Settings,
            dispatcher: Dispatcher,
            *bots: Bot
    ) -> None:

        self.settings = settings
        self.dp = dispatcher
        self.bots = bots

    def register_routers(self, *routers: Router) -> BotApplication:
        self.dp.include_routers(*routers)
        return self

    def register_middlewares(
            self, router: Router, *middlewares: BaseMiddleware
    ) -> BotApplication:

        for middleware in middlewares:
            router.message.middleware.register(middleware)
            router.callback_query.middleware.register(middleware)

        return self

    def register_outer_middlewares(
            self, router: Router, *middlewares: BaseMiddleware
    ) -> BotApplication:

        for middleware in middlewares:
            router.message.outer_middleware.register(middleware)
            router.callback_query.outer_middleware.register(middleware)

        return self

    async def skip_updates(
            self,
            bot: Optional[Bot] = None,
            skip_updates: bool = True
    ) -> None:

        if bot is None:
            for bot in self.bots:
                await bot.delete_webhook(skip_updates)
        else:
            await bot.delete_webhook(skip_updates)

    async def register_commands(
            self,
            *commands: CommandType,
            bot: Optional[Bot] = None,
            **kwargs: Any
    ) -> None:

        cmds = []
        for command in commands:
            cmds.append(BotCommand(**command))

        if bot is None:
            for bot in self.bots:
                await bot.set_my_commands(cmds, **kwargs)
        else:
            await bot.set_my_commands(cmds, **kwargs)

    async def start(self, **kwargs: Any) -> Any:
        await self.dp.start_polling(
            *self.bots,
            **kwargs
        )

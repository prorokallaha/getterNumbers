import asyncio
import logging

from aiogram import Router

from src.common.markers import SessionGatewayMarker, TransactionGatewayMarker
from src.common.sdi import DependencyContainer
from src.core import (
    Settings,
    load_bot,
    load_dispatcher,
    load_settings,
    load_storage,
)
from src.database import (
    database_gateway_factory,
    sa_unit_of_work_factory,
    session_gateway,
    transaction_gateway,
)
from src.database.core.connection import create_sa_engine, create_sa_session_factory
from src.middlewares import (
    ChatMiddleware,
    ErrorMiddleware,
    ThrottlingMiddleware,
    register_middlewares,
)
from src.routers import register_routers
from src.routers.admin.router import admin_router
from src.routers.client.router import client_router
from src.utils.interactions import DatabaseDataPaginationMediator
from src.utils.logger import Logger


async def main() -> None:
    logger = Logger("bot", level=logging.DEBUG)  # in debug mode
    settings = load_settings()

    engine = create_sa_engine(settings.db.url)
    session_factory = create_sa_session_factory(engine)
    container = DependencyContainer()
    container[Settings] = settings
    container[TransactionGatewayMarker] = lambda: transaction_gateway(session_factory())
    container[SessionGatewayMarker] = lambda: session_gateway(session_factory())
    router = Router(name="main")
    storage = load_storage(settings)
    bot = load_bot(settings)
    dispatcher = load_dispatcher(storage)
    await bot.delete_webhook(drop_pending_updates=True)
    register_routers(router, client_router, admin_router)
    register_middlewares(
        router, ThrottlingMiddleware(storage), ErrorMiddleware(logger), is_outer=True
    )
    register_middlewares(router, ChatMiddleware(), is_outer=False)
    dispatcher.include_router(router)
    logger.debug("Bot starting... ")
    try:
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
            logger=logger,
            settings=settings,
            pagination=DatabaseDataPaginationMediator(),
            gateway=lambda: database_gateway_factory(
                sa_unit_of_work_factory(session_factory())
            ),
        )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

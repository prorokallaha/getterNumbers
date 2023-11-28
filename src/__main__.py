import asyncio

from src.core import BotApplication, load_settings
from src.core.loader import load_bot, load_dispatcher, load_storage
from src.database import (
    build_sa_engine,
    build_sa_session_factory,
)
from src.middlewares import ChatMiddleware, ErrorMiddleware
from src.routers import router
from src.utils.interactions import DatabaseDataPaginationMediator
from src.utils.logger import Logger


async def main() -> None:
    settings = load_settings()
    storage = load_storage(settings)
    dispatcher = load_dispatcher(storage)
    app = BotApplication(settings, dispatcher, load_bot(settings))
    app.register_routers(router)
    app.register_middlewares(router, ErrorMiddleware(Logger("error")), ChatMiddleware())
    await app.skip_updates()
    await app.register_commands(
        {"command": "/start", "description": "Команда для начала общения с ботом"}
    )
    engine = build_sa_engine(
        settings.db.url,
        echo=settings.db.echo,
        future=settings.db.future
    )
    session_pool = build_sa_session_factory(engine)
    try:
        await app.start(
            allow_updates=dispatcher.resolve_used_update_types(),
            pagination=DatabaseDataPaginationMediator(),
            db_pool=session_pool,
            admins=settings.bot.admins,
        )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

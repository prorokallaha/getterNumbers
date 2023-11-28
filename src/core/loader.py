from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage

from src.core.settings import Settings


def load_storage(settings: Settings) -> BaseStorage:

    try:
        import redis.asyncio as aioredis
        from aiogram.fsm.storage.redis import RedisStorage
        storage = RedisStorage(redis=aioredis.Redis(**settings.redis_settings))
    except ImportError:
        from aiogram.fsm.storage.memory import MemoryStorage
        storage = MemoryStorage() # type: ignore

    return storage


def load_dispatcher(
        storage: Optional[BaseStorage] = None
) -> Dispatcher:
    return Dispatcher(storage=storage)


def load_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        parse_mode=settings.parse_mode,
        disable_web_page_preview=settings.disable_web_page_preview,
        protect_content=settings.protect_content
    )

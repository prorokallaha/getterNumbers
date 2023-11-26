from typing import Any, AsyncGenerator, TypeAlias

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

SessionPoolType: TypeAlias = async_sessionmaker[AsyncSession]


def build_sa_engine(url: str, **options: Any) -> AsyncEngine:
    return create_async_engine(url, **options)


def build_sa_session_factory(
        engine: AsyncEngine
) -> SessionPoolType:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def build_sa_session(
        session_factory: SessionPoolType
) -> AsyncGenerator[Any, AsyncSession]:

    async with session_factory() as session:
        yield session

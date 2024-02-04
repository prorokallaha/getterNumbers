import asyncio
import random

from src.common.dto.user import UserCreate
from src.common.sdi import DependencyContainer, Depends, inject
from src.core import load_settings
from src.database import (
    DatabaseGateway,
    database_gateway_factory,
    sa_unit_of_work_factory,
)
from src.database.core.connection import (
    SessionFactoryType,
    create_sa_engine,
    create_sa_session_factory,
)
class EX:
    ...
class GGG:
    ...

@inject
async def get_(gg: int = Depends(EX), gggg: int = Depends(GGG)) -> None:
    print(gg)
    print(gggg)
    for i in range(10):
        yield i
    # await cxzczx()

def ex() -> int:
    yield 15

async def ggg() -> int:
    yield 255

async def go() -> None:
    return await get_()


async def xxx(session_factory: SessionFactoryType) -> DatabaseGateway:
    gateway = database_gateway_factory(sa_unit_of_work_factory(session_factory()))
    async with gateway:
        yield gateway


async def main() -> None:
    settings = load_settings()
    container = DependencyContainer()
    engine = create_sa_engine(settings.db.url)
    f = create_sa_session_factory(engine)
    container[DatabaseGateway] = lambda: xxx(f)
    container[EX] = ex
    container[GGG] = ggg
    # tasks = [asyncio.create_task(go(), name=str(i)) for i in range(10000)]
    async for i in await get_():
        print(i)

    # for i in range(100):
    #     await go()
    # await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

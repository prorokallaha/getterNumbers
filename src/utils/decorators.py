from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.services.database.gateway import service_gateway_factory

P = ParamSpec('P')
R = TypeVar('R')

def with_database_service(
        select_only: bool = False
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:

    def _wrapper(
            handler: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:

        @wraps(handler)
        async def _inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:

            if (session_factory := kwargs.get('session_factory')) is None:
                raise TypeError(
                    'session_factory does not exists in function signature'
                )

            if not callable(session_factory):
                raise TypeError('session_factory param must be a callable type')

            if not isinstance(session_factory, async_sessionmaker):
                raise TypeError(
                    f'session_factory function must returning async_sessionmaker type, not {type(session_factory).__name__}'
                )
            session = session_factory()
            gateway = service_gateway_factory(session)
            kwargs['service'] = gateway
            if select_only:
                async with session:
                    return await handler(*args, **kwargs)
            async with gateway:
                return await handler(*args, **kwargs)

        return _inner_wrapper

    return _wrapper

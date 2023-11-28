from functools import wraps
from typing import Any, Awaitable, Callable, ParamSpec

from src.services.database import service_gateway_factory

P = ParamSpec('P')

def with_database_service(
        handler: Callable[P, Awaitable[Any]]
) -> Callable[P, Awaitable[Any]]:

    @wraps(handler)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        session = kwargs['db_pool']
        async with service_gateway_factory(session()) as service: # type: ignore
            kwargs['service'] = service
            return await handler(*args, **kwargs)

    return _wrapper

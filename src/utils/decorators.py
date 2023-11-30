from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from src.common.services.gateway import AbstractServiceGateway

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
            try:
                service = kwargs['service']
            except KeyError as e:
                raise TypeError(
                    'service does not exists in function signature'
                ) from e

            if not callable(service):
                raise TypeError('service param must be a callable type')

            if (gateway := service()) and not isinstance(gateway, AbstractServiceGateway):
                raise TypeError(
                    f'service function must returning Gateway type, not {type(gateway).__name__}'
                )

            kwargs['service'] = gateway
            if select_only:
                return await handler(*args, **kwargs)
            async with gateway:
                return await handler(*args, **kwargs)

        return _inner_wrapper

    return _wrapper

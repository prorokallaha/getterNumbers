import asyncio
import inspect
from functools import wraps
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    ParamSpec,
    TypeVar,
    Union,
    overload,
)

import src.common.sdi.depends as depends
from src.common.sdi.container import DependencyContainer, KeyType
from src.common.sdi.exits import AsyncExit, SyncExit

__all__ = (
    "DependencyContainer",
    "Depends",
    "inject",
)

R = TypeVar("R")
P = ParamSpec("P")


def Depends(dependency: KeyType, *, use_cache: bool = False) -> Any:
    return depends.Depends(dependency, use_cache=use_cache)


@overload
def inject(__coro: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    ...


@overload
def inject(__coro: Callable[P, AsyncIterator[R]]) -> Callable[P, AsyncIterator[R]]:
    ...


@overload
def inject(__func: Callable[P, Iterator[R]]) -> Callable[P, Iterator[R]]:
    ...


@overload
def inject(__func: Callable[P, R]) -> Callable[P, R]:
    ...


def inject(__func_or_coro: Any) -> Any:
    origin_signature = inspect.signature(__func_or_coro)
    is_async = asyncio.iscoroutinefunction(
        __func_or_coro
    ) or inspect.isasyncgenfunction(__func_or_coro)

    if is_async:
        return wrap_async_injection(__func_or_coro, origin_signature)
    else:
        return wrap_sync_injection(__func_or_coro, origin_signature)


def wrap_sync_injection(
    func: Callable[P, Union[R, Iterator[R]]], signature: inspect.Signature
) -> Callable[P, Union[R, Iterator[R]]]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Union[R, Iterator[R]]:
        resolved_sig = depends._resolve_sync_signature(signature)
        kw = {**kwargs, **resolved_sig}
        with SyncExit():
            return func(*args, **kw)

    return _wrapper


def wrap_async_injection(
    coro: Union[Callable[P, Awaitable[R]], Callable[P, AsyncIterator[R]]],
    signature: inspect.Signature,
) -> Callable[P, Awaitable[Union[R, AsyncIterator[R]]]]:
    @wraps(coro)
    async def _async_wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> Union[R, AsyncIterator[R]]:
        resolved_sig = await depends._resolve_async_signature(signature)
        kw = {**kwargs, **resolved_sig}
        async with AsyncExit():
            if inspect.isasyncgenfunction(coro):
                return coro(*args, **kw)
            else:
                return await coro(*args, **kw)  # type: ignore

    return _async_wrapper

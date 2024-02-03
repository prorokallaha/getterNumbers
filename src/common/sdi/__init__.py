import asyncio
import inspect
from functools import wraps
from typing import (
    Any,
    Callable,
    Coroutine,
    Union,
)

import src.common.sdi.depends as depends
from src.common.sdi.container import DependencyContainer, KeyType
from src.common.sdi.exits import AsyncExit, SyncExit

__all__ = (
    "DependencyContainer",
    "Depends",
    "inject",
)


def Depends(dependency: KeyType, *, use_cache: bool = False) -> Any:
    return depends.Depends(dependency, use_cache=use_cache)


def inject(
    _call: Union[Callable[..., Coroutine[Any, Any, Any]], Callable[..., Any]],
) -> Any:
    origin_signature = inspect.signature(_call)

    @wraps(_call)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        resolved_sig = depends._resolve_sync_signature(origin_signature)
        kw = {**kwargs, **resolved_sig}
        with SyncExit():
            return _call(*args, **kw)

    @wraps(_call)
    async def _async_wrapper(*args: Any, **kwargs: Any) -> Any:
        resolved_sig = await depends._resolve_async_signature(origin_signature)
        kw = {**kwargs, **resolved_sig}
        async with AsyncExit():
            if inspect.isasyncgenfunction(_call):
                return _call(*args, **kw)
            return await _call(*args, **kw)

    is_async = asyncio.iscoroutinefunction(_call) or inspect.isasyncgenfunction(_call)
    if is_async:
        return _async_wrapper
    else:
        return _wrapper

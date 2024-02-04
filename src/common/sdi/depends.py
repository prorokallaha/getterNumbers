from __future__ import annotations

import asyncio
import inspect
from typing import Annotated, Any, Dict, Generic, List, Tuple, cast, get_origin

from src.common.sdi.container import DependencyContainer, DependencyType, KeyType
from src.common.sdi.exits import AsyncExit, SyncExit


class Depends(Generic[KeyType, DependencyType]):
    __slots__ = (
        "_container",
        "_dependency",
        "_use_cache",
        "_cache",
        "_async_exit",
        "_sync_exit",
    )

    def __init__(
        self,
        dependency: KeyType,
        *,
        use_cache: bool = False,
    ) -> None:
        self._container = DependencyContainer()
        self._dependency = dependency
        self._use_cache = use_cache
        self._cache: Dict[KeyType, DependencyType] = {}
        self._async_exit = AsyncExit()
        self._sync_exit = SyncExit()

    async def resolve_async(self) -> DependencyType:
        if self._dependency in self._cache:
            return self._cache[self._dependency]
        dependency = self._container[self._dependency]
        if dependency is None:
            raise ValueError(f"No dependency found for type {self._dependency}")

        if callable(dependency):
            result = dependency()
            if inspect.isgenerator(result):
                self._async_exit.gens.append(result)
                result = next(result)
            elif asyncio.iscoroutine(result):
                result = await result
            elif inspect.isasyncgen(result):
                self._async_exit.gens.append(result)
                result = await anext(result)
        else:
            result = dependency

        if self._use_cache:
            self._cache[self._dependency] = result

        return cast(DependencyType, result)

    def resolve_sync(self) -> DependencyType:
        if self._dependency in self._cache:
            return self._cache[self._dependency]

        dependency = self._container[self._dependency]
        if dependency is None:
            raise ValueError(f"No dependency found for type {self._dependency}")

        if callable(dependency):
            result = dependency()
            if inspect.isgenerator(result):
                self._sync_exit.gens.append(result)
                result = next(result)
        else:
            result = dependency

        if self._use_cache:
            self._cache[self._dependency] = result

        return cast(DependencyType, result)


def _resolve_sync_signature(
    signature: inspect.Signature,
) -> Tuple[List[SyncExit], Dict[str, Any]]:
    resolved_signature = {}
    exits = []
    for _, v in signature.parameters.items():
        param = v.default
        if isinstance(param, Depends):
            exits.append(param._sync_exit)
            resolved_signature[v.name] = param.resolve_sync()
        if get_origin(v.annotation) is Annotated:
            metadata = v.annotation.__metadata__
            if metadata and isinstance(metadata[0], Depends):
                exits.append(param._sync_exit)
                resolved_signature[v.name] = metadata[0].resolve_sync()

    return exits, resolved_signature


async def _resolve_async_signature(
    signature: inspect.Signature,
) -> Tuple[List[AsyncExit], Dict[str, Any]]:
    resolved_signature = {}
    exits = []
    for _, v in signature.parameters.items():
        param = v.default
        if isinstance(param, Depends):
            exits.append(param._async_exit)
            resolved_signature[v.name] = await param.resolve_async()

        if get_origin(v.annotation) is Annotated:
            metadata = v.annotation.__metadata__
            if metadata and isinstance(metadata[0], Depends):
                exits.append(param._async_exit)
                resolved_signature[v.name] = await metadata[0].resolve_async()
    return exits, resolved_signature

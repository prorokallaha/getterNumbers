from __future__ import annotations

import asyncio
import inspect
from typing import Annotated, Any, Callable, Dict, Union, get_origin

from src.common.sdi.container import DependencyContainer, DependencyType, KeyType
from src.common.sdi.exits import AsyncExit, SyncExit


class Depends:
    __slots__ = (
        "_container",
        "_dependency",
        "_use_cache",
        "_cache",
    )

    def __init__(self, dependency: KeyType, *, use_cache: bool = False) -> None:
        self._container = DependencyContainer()
        self._dependency = self._extract_dep_type(dependency)
        self._use_cache = use_cache
        self._cache = {}

    async def resolve_async(self) -> Any:
        if self._dependency in self._cache:
            return self._cache[self._dependency]
        dependency = self._container[self._dependency]
        if dependency is None:
            raise ValueError(f"No dependency found for type {self._dependency}")

        if callable(dependency):
            result = dependency()
            if asyncio.iscoroutine(result):
                result = await result
            elif inspect.isasyncgen(result):
                AsyncExit._exits.append(result)
                result = await anext(result)
        else:
            result = dependency

        if self._use_cache:
            self._cache[self._dependency] = result

        return result

    def resolve_sync(self) -> Any:
        if self._dependency in self._cache:
            return self._cache[self._dependency]

        dependency = self._container[self._dependency]
        if dependency is None:
            raise ValueError(f"No dependency found for type {self._dependency}")

        if callable(dependency):
            result = dependency()
            if inspect.isgenerator(result):
                SyncExit._exits.append(result)
                result = next(result)
        else:
            result = dependency

        if self._use_cache:
            self._cache[self._dependency] = result

        return result

    def _extract_dep_type(
        self, dependency: KeyType
    ) -> Union[DependencyType, Callable[..., DependencyType]]:
        if hasattr(dependency, "__metadata__") and dependency.__metadata__:
            metadata = dependency.__metadata__[0]
            if isinstance(metadata, Depends):
                return metadata._dependency
        return dependency


def _resolve_sync_signature(
    signature: inspect.Signature,
) -> Dict[str, Any]:
    resolved_signature = {}
    for _, v in signature.parameters.items():
        param = v.default
        if isinstance(param, Depends):
            resolved_signature[v.name] = param.resolve_sync()
        if get_origin(v.annotation) is Annotated:
            metadata = v.annotation.__metadata__
            if metadata and isinstance(metadata[0], Depends):
                resolved_signature[v.name] = metadata[0].resolve_sync()

    return resolved_signature


async def _resolve_async_signature(
    signature: inspect.Signature,
) -> Dict[str, Any]:
    resolved_signature = {}
    for _, v in signature.parameters.items():
        param = v.default
        if isinstance(param, Depends):
            resolved_signature[v.name] = await param.resolve_async()

        if get_origin(v.annotation) is Annotated:
            metadata = v.annotation.__metadata__
            if metadata and isinstance(metadata[0], Depends):
                resolved_signature[v.name] = await metadata[0].resolve_async()

    return resolved_signature

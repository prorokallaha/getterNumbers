from __future__ import annotations

import inspect
from typing import Any

from src.common.sdi._meta import Singleton


class SyncExit(metaclass=Singleton):
    _exits = []

    def __enter__(self) -> SyncExit:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        for gen in reversed(self._exits):
            try:
                if inspect.isgenerator(gen):
                    next(gen)
            except StopIteration:
                pass
            except StopAsyncIteration:
                pass
        self._exits.clear()


class AsyncExit(metaclass=Singleton):
    _exits = []

    async def __aenter__(self) -> AsyncExit:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        for gen in reversed(self._exits):
            try:
                if inspect.isasyncgen(gen):
                    await anext(gen)
                elif inspect.isgenerator(gen):
                    next(gen)
            except StopIteration:
                pass
            except StopAsyncIteration:
                pass
        self._exits.clear()

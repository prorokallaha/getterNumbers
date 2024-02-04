from __future__ import annotations

import inspect
from typing import Any


class SyncExit:
    __slots__ = ("gens",)

    def __init__(self) -> None:
        self.gens = []

    def __enter__(self) -> SyncExit:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        for gen in reversed(self.gens):
            try:
                if inspect.isgenerator(gen):
                    next(gen)
            except StopIteration:
                pass


class AsyncExit:
    __slots__ = ("gens",)

    def __init__(self) -> None:
        self.gens = []

    async def __aenter__(self) -> AsyncExit:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        for gen in reversed(self.gens):
            try:
                if inspect.isasyncgen(gen):
                    await anext(gen)
                elif inspect.isgenerator(gen):
                    next(gen)
            except StopIteration:
                pass
            except StopAsyncIteration:
                pass

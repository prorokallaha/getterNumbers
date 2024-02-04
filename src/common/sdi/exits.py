from __future__ import annotations

import inspect
from typing import Any

from src.common.sdi._meta import Singleton


class SyncExit(metaclass=Singleton):
    exits = {}
    depends = []

    def __enter__(self) -> SyncExit:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        for dep in reversed(self.depends):
            gen = self.exits.pop(dep, None)
            if gen is None:
                continue
            self.depends.remove(dep)
            try:
                if inspect.isgenerator(gen):
                    next(gen)
            except StopIteration:
                pass


class AsyncExit(metaclass=Singleton):
    exits = {}
    depends = []

    async def __aenter__(self) -> AsyncExit:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        for dep in reversed(self.depends):
            gen = self.exits.pop(dep, None)
            if gen is None:
                continue
            self.depends.remove(dep)
            try:
                if inspect.isasyncgen(gen):
                    await anext(gen)
                elif inspect.isgenerator(gen):
                    next(gen)
            except StopIteration:
                pass
            except StopAsyncIteration:
                pass

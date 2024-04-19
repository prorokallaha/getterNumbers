from typing import Any, Protocol, Type


class Repository(Protocol):
    model: Type[Any]

from typing import Any, Optional, Protocol


class MediatorType(Protocol):

    def add(
            self,
            instance: Any,
            name: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    def get(self, key: str) -> Any:
        raise NotImplementedError


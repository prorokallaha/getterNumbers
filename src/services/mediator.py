from typing import Any, Dict, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.database.base import BaseDBService


class ServiceMediator:

    def __init__(self) -> None:
        self._services: Dict[str, BaseDBService[Any]] = {}

    def add(
            self,
            service_instance: BaseDBService[Any],
            service_name: Optional[str] = None
    ) -> None:

        self._services[
            service_name or type(service_instance).__name__.lower()
            ] = service_instance

    def __getattr__(self, key: str) -> Any:

        if key in self._services:
            return self._services[key]

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key: str, value: Any) -> None:

        if key != '_services':
            self._services[key] = value
        else:
            super().__setattr__(key, value)


def build_mediator(
        session: AsyncSession,
        *services: Type[BaseDBService[Any]]
) -> ServiceMediator:

    mediator = ServiceMediator()

    for service in services:
        mediator.add(service(session))

    return mediator

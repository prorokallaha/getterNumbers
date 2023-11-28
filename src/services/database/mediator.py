from typing import Any, Mapping, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database.interfaces.repositories.crud import AbstractCRUDRepository
from src.database.repositories.crud import ModelT
from src.services.database.services.base import BaseService


class ServiceMediator:

    def __init__(self) -> None:
        self._services = {}

    def add(
            self,
            service_instance: BaseService[ModelT],
            service_name: Optional[str] = None
    ) -> None:
        self._services[
            service_name or type(service_instance).__name__.lower()
        ] = service_instance

    def get(self, key: str) -> Optional[BaseService[ModelT]]:
        return self._services.get(key)

    def __getattr__(self, key: str) -> Any:
        if key in self._services:
            return self._services[key]

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key: str, value: Any) -> None:
        if key != "_services":
            self._services[key] = value
        else:
            super().__setattr__(key, value)


def build_mediator(
    session: AsyncSession,
    crud: Type[AbstractCRUDRepository[AsyncSession, ModelT]],
    services: Mapping[Type[ModelT], Type[BaseService[ModelT]]],
) -> ServiceMediator:

    mediator = ServiceMediator()

    for model, service in services.items():
        mediator.add(service(crud(session, model)))

    return mediator

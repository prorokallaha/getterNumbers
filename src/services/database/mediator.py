from typing import (
    Any,
    Dict,
    Mapping,
    Optional,
    Type,
)

from src.common.database.interfaces.repositories.crud import AbstractCRUDRepository
from src.common.services.service import ServiceType
from src.common.types import SessionType
from src.database.repositories.crud import ModelT


class ServiceMediator:

    def __init__(self) -> None:
        self._services: Dict[str, ServiceType] = {}

    def add(
            self,
            instance: ServiceType,
            name: Optional[str] = None
    ) -> None:
        self._services[
            name or type(instance).__name__.lower()
        ] = instance

    def get(self, key: str) -> Optional[ServiceType]:
        return self._services.get(key)

    def __getattr__(self, key: str) -> Any:
        try:
            return self._services[key]
        except KeyError as err:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'"
            ) from err

    def __setattr__(self, key: str, value: Any) -> None:
        if key != "_services":
            self._services[key] = value
        else:
            super().__setattr__(key, value)


def build_mediator(
    session: SessionType,
    crud_repo: Type[AbstractCRUDRepository[SessionType, ModelT]],
    services: Mapping[Type[ModelT], Type[ServiceType]],
) -> ServiceMediator:

    mediator = ServiceMediator()

    for model, service in services.items():
        mediator.add(service(crud_repo(session, model)))

    return mediator

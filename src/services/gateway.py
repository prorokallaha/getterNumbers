from __future__ import annotations

from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core.unit_of_work import SQLALchemyUnitOfWork
from src.services import SERVICES
from src.services.database.user import UserService
from src.services.mediator import ServiceMediator, build_mediator


class ServiceGateway:

    __slots__ = (
        '_uow',
        '_mediator',
    )

    def __init__(
            self,
            unit_of_work: SQLALchemyUnitOfWork,
            mediator: ServiceMediator
    ) -> None:

        self._uow = unit_of_work
        self._mediator = mediator

    async def __aenter__(self) -> ServiceGateway:
        await self._uow.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._uow.__aexit__(*args)

    @property
    def user(self) -> UserService:
        return cast(UserService, self._mediator.userservice)


def service_gateway_factory(session: AsyncSession) -> ServiceGateway:

    return ServiceGateway(
        SQLALchemyUnitOfWork(session),
        build_mediator(session, *SERVICES)
    )

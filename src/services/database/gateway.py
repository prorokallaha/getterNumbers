from __future__ import annotations

from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.services.gateway import AbstractServiceGateway
from src.database.core.unit_of_work import SQLALchemyUnitOfWork
from src.database.repositories.crud import SQLAlchemyCRUDRepository
from src.services.database.mediator import build_mediator
from src.services.database.services import SERVICES
from src.services.database.services.user import UserService


class ServiceGateway(AbstractServiceGateway):

    @property
    def user(self) -> UserService:
        return cast(UserService, self._mediator.get('userservice'))


def service_gateway_factory(session: AsyncSession) -> ServiceGateway:

    return ServiceGateway(
        SQLALchemyUnitOfWork(session),
        build_mediator(session, SQLAlchemyCRUDRepository, SERVICES)
    )

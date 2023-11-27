from src.services.database.user import UserService
from src.services.gateway import ServiceGateway, service_gateway_factory

__all__ = (
    'ServiceGateway',
    'service_gateway_factory',
)

SERVICES = (
    UserService,
)

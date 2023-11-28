from src.database.models.user import User
from src.services.database.services.user import UserService

__all__ = (
    'UserService',
)

SERVICES = {
    User: UserService,
}

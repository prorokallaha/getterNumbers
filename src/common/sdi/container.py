from typing import (
    Callable,
    Dict,
    Generic,
    TypeVar,
    Union,
)

from src.common.sdi._meta import Singleton

KeyType = TypeVar("KeyType")
DependencyType = TypeVar("DependencyType")


class DependencyContainer(Generic[KeyType, DependencyType], metaclass=Singleton):
    __slots__ = ("_dependencies",)

    def __init__(self) -> None:
        self._dependencies: Dict[
            KeyType,
            Union[DependencyType, Callable[..., DependencyType]],
        ] = {}

    def register(
        self,
        key: KeyType,
        value: Union[DependencyType, Callable[..., DependencyType]],
    ) -> None:
        self._dependencies[key] = value

    def get(
        self,
        key: KeyType,
    ) -> Union[DependencyType, Callable[..., DependencyType]]:
        return self._dependencies[key]

    def __getitem__(
        self,
        key: KeyType,
    ) -> Union[DependencyType, Callable[..., DependencyType]]:
        return self.get(key)

    def __setitem__(
        self,
        key: KeyType,
        value: Union[DependencyType, Callable[..., DependencyType]],
    ) -> None:
        self._dependencies[key] = value

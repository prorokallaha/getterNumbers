from typing import (
    Any,
    Callable,
    Dict,
    Type,
    TypeVar,
    Union,
)

from src.common.sdi._meta import Singleton

KeyType = TypeVar("KeyType", bound=Any)
DependencyType = TypeVar("DependencyType", bound=Any)


class DependencyContainer(metaclass=Singleton):
    __slots__ = ("_dependencies",)

    def __init__(self) -> None:
        self._dependencies: Dict[Any, Union[Any, Callable[..., Any]]] = {}

    def register(
        self, key: KeyType, value: Union[DependencyType, Callable[..., Any]]
    ) -> None:
        self._dependencies[key] = value

    def get(
        self, key: Union[KeyType, Type[DependencyType]]
    ) -> Union[DependencyType, Callable[..., Any]]:
        return self._dependencies[key]

    def __getattr__(self, name: KeyType) -> Any:
        try:
            return self._dependencies[name]
        except KeyError as e:
            raise AttributeError(f"No dependency found for {name}") from e

    def __setattr__(
        self, name: KeyType, value: Union[DependencyType, Callable[..., Any]]
    ) -> None:
        if name == "_dependencies":
            super().__setattr__(name, value)
        else:
            self._dependencies[name] = value

    def __getitem__(self, key: KeyType) -> Union[DependencyType, Callable[..., Any]]:
        return self.get(key)

    def __setitem__(
        self, key: KeyType, value: Union[DependencyType, Callable[..., Any]]
    ) -> None:
        self._dependencies[key] = value

import typing
from abc import ABC, abstractmethod
from .autoscaler import AutoScaler


T = typing.TypeVar('T', int, float, str)


ArgumentType: typing.TypeAlias = typing.Union[T, typing.Callable[[], T]]


class BuiltinAutoScaler(ABC, AutoScaler):
    ArgumentType = typing.Union[T, typing.Callable[[], T]]

    @classmethod
    @abstractmethod
    def autoscaler_name(cls) -> str: ...

    @abstractmethod
    def autoscaler_arguments(self) -> typing.Dict[str, ArgumentType]: ...


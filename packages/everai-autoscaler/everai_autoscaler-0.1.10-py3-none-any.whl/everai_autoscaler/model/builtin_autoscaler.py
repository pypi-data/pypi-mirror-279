from __future__ import annotations
import typing
from abc import ABC, abstractmethod
from .autoscaler import AutoScaler


T = typing.TypeVar('T', int, float, str)


ArgumentType: typing.TypeAlias = typing.Union[T, typing.Callable[[], T]]


class BuiltinAutoScaler(AutoScaler):
    ArgumentType = typing.Union[T, typing.Callable[[], T]]

    @classmethod
    @abstractmethod
    def autoscaler_name(cls) -> str: ...

    @classmethod
    @abstractmethod
    def from_arguments(cls, arguments: typing.Dict[str, str]) -> BuiltinAutoScaler: ...


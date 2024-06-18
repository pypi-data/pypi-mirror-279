from __future__ import annotations
import typing
from abc import abstractmethod

from . import Factors, DecideResult
from .autoscaler import AutoScaler


T = typing.TypeVar('T', int, float, str)


ArgumentType: typing.TypeAlias = typing.Union[T, typing.Callable[[], T]]


class BuiltinAutoScaler(AutoScaler):
    @abstractmethod
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    @abstractmethod
    def scheduler_name(cls) -> str: ...

    @classmethod
    @abstractmethod
    def autoscaler_name(cls) -> str: ...

    @abstractmethod
    def autoscaler_arguments(self) -> typing.Dict[str, ArgumentType]: ...

    @classmethod
    @abstractmethod
    def from_arguments(cls, arguments: typing.Dict[str, str]) -> BuiltinAutoScaler: ...


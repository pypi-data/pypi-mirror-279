import typing

from .factors import Factors
from .action import  DecideResult
from .autoscaler import AutoScaler

T = typing.TypeVar('T', int, float, str)


ArgumentType: typing.TypeAlias = typing.Union[T, typing.Callable[[], T]]

class BuiltinAutoScaler(AutoScaler):
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    def scheduler_name(cls) -> str: ...

    @classmethod
    def autoscaler_name(cls) -> str: ...

    def autoscaler_arguments(self) -> typing.Dict[str, ArgumentType]: ...

    @classmethod
    def from_arguments(cls, arguments: typing.Dict[str, str]) -> BuiltinAutoScaler: ...

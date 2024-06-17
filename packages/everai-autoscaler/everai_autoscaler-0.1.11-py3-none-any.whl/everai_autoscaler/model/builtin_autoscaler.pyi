import typing

from everai_autoscaler.model.factors import Factors
from .action import  DecideResult

T = typing.TypeVar('T', int, float, str)


ArgumentType: typing.TypeAlias = typing.Union[T, typing.Callable[[], T]]

class BuiltinAutoScaler:
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    def scheduler_name(cls) -> str: ...

    @classmethod
    def autoscaler_name(cls) -> str: ...

    @classmethod
    def from_arguments(cls, arguments: typing.Dict[str, str]) -> BuiltinAutoScaler: ...

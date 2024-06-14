import typing

from .factors import Factors
from .action import  DecideResult

T = typing.TypeVar('T', int, float, str)


ArgumentType: typing.TypeAlias = typing.Union[T, typing.Callable[[], T]]

class BuiltinAutoScaler:
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    def scheduler_name(cls) -> str: ...

    @classmethod
    def autoscaler_name(cls) -> str: ...

    def autoscaler_arguments(self) -> typing.Dict[str, ArgumentType]: ...

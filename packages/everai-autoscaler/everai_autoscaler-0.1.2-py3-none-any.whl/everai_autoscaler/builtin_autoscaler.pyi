import typing

from .factors import Factors
from .action import  DecideResult

class BuiltinAutoScaler:
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    def scheduler_name(cls) -> str: ...

    @classmethod
    def autoscaler_name(cls) -> str: ...

    def autoscaler_arguments(self) -> typing.Dict[str, str]: ...

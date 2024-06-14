import typing
from abc import ABC, abstractmethod
from .autoscaler import AutoScaler


class BuiltinAutoScaler(ABC, AutoScaler):
    @classmethod
    @abstractmethod
    def autoscaler_name(cls) -> str: ...

    @abstractmethod
    def autoscaler_arguments(self) -> typing.Dict[str, str]: ...


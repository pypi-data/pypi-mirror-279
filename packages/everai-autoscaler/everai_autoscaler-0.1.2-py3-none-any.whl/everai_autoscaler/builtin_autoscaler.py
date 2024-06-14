import typing
from abc import ABC, abstractmethod


class BuiltinAutoScaler(ABC):
    @classmethod
    @abstractmethod
    def autoscaler_name(cls) -> str: ...

    @abstractmethod
    def autoscaler_arguments(self) -> typing.Dict[str, str]: ...


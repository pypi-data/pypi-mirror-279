from abc import ABC, abstractmethod
from .factors import Factors
from .action import DecideResult


class AutoScaler(ABC):
    @abstractmethod
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    @abstractmethod
    def scheduler_name(cls) -> str: ...

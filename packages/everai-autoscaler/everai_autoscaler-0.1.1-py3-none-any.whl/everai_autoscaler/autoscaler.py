from abc import ABC, abstractmethod
import typing
from datetime import datetime

from .factors import Factors
from .action import DecideResult


class AutoScaler(ABC):
    @abstractmethod
    def decide(self, factors: Factors) -> DecideResult: ...

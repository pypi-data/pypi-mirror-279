from .factors import Factors
from .action import DecideResult

class AutoScaler:
    def decide(self, factors: Factors) -> DecideResult: ...

    @classmethod
    def scheduler_name(cls) -> str: ...
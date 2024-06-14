from everai.autoscaling.factors import Factors
from everai.autoscaling.action import DecideResult

class AutoScaler:
    def decide(self, factors: Factors) -> DecideResult: ...

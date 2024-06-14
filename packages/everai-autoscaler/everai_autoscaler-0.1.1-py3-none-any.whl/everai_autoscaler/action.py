from __future__ import annotations

import json
import typing
from pydantic import BaseModel, Field


class ScaleUpAction(BaseModel):
    count: int
    action: str = Field(default='ScaleUp')

    @staticmethod
    def from_json(data) -> ScaleUpAction:
        return ScaleUpAction.model_validate_json(data)


class ScaleDownAction(BaseModel):
    worker_id: str
    action: str = Field(default='ScaleDown')

    @staticmethod
    def from_json(data) -> ScaleDownAction:
        return ScaleDownAction.model_validate_json(data)


Action = typing.Union[ScaleUpAction, ScaleDownAction]


class DecideResult(BaseModel):
    max_workers: int
    actions: typing.List[Action]

    @staticmethod
    def from_json(data) -> DecideResult:
        return DecideResult.model_validate_json(data)


def actions_to_json(actions: typing.List[Action]) -> str:
    return json.dumps([act.dict() for act in actions])


# coding: utf-8
from __future__ import annotations

import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, StrictInt

from xingchen.models.custom.completion.completion_resp_message import AcARespMessage


class AcAChoice(BaseModel):
    index: Optional[StrictInt] = Field(None, alias="index")
    finish_reason: Optional[StrictStr] = Field(None, alias="finish_reason")
    message: Optional[AcARespMessage] = Field(None, alias="message")

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.dict(by_alias=True, exclude={}, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> AcAChoice:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> AcAChoice:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AcAChoice.parse_obj(obj)

        return AcAChoice.parse_obj({
            'index': obj.get('index'),
            'finish_reason': obj.get('finish_reason'),
            'message': AcARespMessage.from_dict(obj.get('message')) if obj.get('message') is not None else None
        })

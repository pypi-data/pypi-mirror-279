from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import Field, conlist

from xingchen.models.platform_plugin import PlatformPlugin
from xingchen.models.reject_condition import RejectCondition


class RejectAnswerPlugin(PlatformPlugin):
    reject_conditions: Optional[conlist(RejectCondition)] = Field(None, alias="rejectConditions")
    __properties = ["rejectConditions"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RejectAnswerPlugin:
        """Create an instance of RejectAnswerPlugin from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RejectAnswerPlugin:
        """Create an instance of RejectAnswerPlugin from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PlatformPlugin.parse_obj(obj)

        _obj = PlatformPlugin.parse_obj({
            "enabled": obj.get("enabled"),
            "name": obj.get("name"),
            "reject_conditions": [RejectCondition.from_dict(_item) for _item in obj.get("rejectConditions")] if obj.get("rejectConditions") is not None else None
        })
        return _obj

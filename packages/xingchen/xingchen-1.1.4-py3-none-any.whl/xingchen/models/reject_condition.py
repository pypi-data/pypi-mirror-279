from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import Field, StrictStr, StrictBool, BaseModel, conlist

from xingchen.models.keyword import Keyword


class RejectCondition(BaseModel):
    enabled: Optional[StrictBool] = None
    condition_type: Optional[StrictStr] = Field(None, alias="conditionType")
    keywords: Optional[conlist(Keyword)] = Field(None, alias="keywords")
    sub_reject_condition: Optional[RejectCondition] = Field(None, alias="subRejectCondition")
    __properties = ["enabled", "conditionType", "keywords", "subRejectCondition"]

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
    def from_json(cls, json_str: str) -> RejectCondition:
        """Create an instance of RejectCondition from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RejectCondition:
        """Create an instance of RejectCondition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RejectCondition.parse_obj(obj)

        _obj = RejectCondition.parse_obj({
            "enabled": obj.get("enabled"),
            "condition_type": obj.get("conditionType"),
            "keywords": [Keyword.from_dict(_item) for _item in obj.get("keywords")] if obj.get(
                "keywords") is not None else None,
            "sub_reject_condition": RejectCondition.from_dict(obj.get("subRejectCondition")) if obj.get(
                "subRejectCondition") is not None else None
        })
        return _obj

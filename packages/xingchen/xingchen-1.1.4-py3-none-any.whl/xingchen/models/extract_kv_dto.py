from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, conlist

from xingchen.models import Context
from xingchen.models.custom import Usage
from xingchen.models.extract_data import ExtractData


class ExtractKVDTO(BaseModel):
    schemas: Optional[conlist(ExtractData)] = Field(None, alias="schemas")
    usage: Optional[Usage] = Field(None, alias="usage")
    context: Optional[Context] = Field(None, alias="context")
    __properties = ["schemas", "usage", "context"]

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
    def from_json(cls, json_str: str) -> ExtractKVDTO:
        """Create an instance of ExtractKVDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExtractKVDTO:
        """Create an instance of ExtractKVDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExtractKVDTO.parse_obj(obj)

        _obj = ExtractKVDTO.parse_obj({
            "schemas": [ExtractData.from_dict(_item) for _item in obj.get("schemas")] if obj.get(
                "schemas") is not None else None,
            "usage": Usage.from_dict(obj.get("usage")) if obj.get("usage") is not None else None,
            "context": Context.from_dict(obj.get("context")) if obj.get("context") is not None else None
        })
        return _obj

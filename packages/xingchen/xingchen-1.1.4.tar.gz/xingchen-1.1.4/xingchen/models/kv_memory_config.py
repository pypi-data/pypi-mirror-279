from __future__ import annotations
import pprint
import re
import json

from typing import Optional
from pydantic import BaseModel, Field, StrictStr, StrictBool


class KVMemoryConfig(BaseModel):
    enabled: Optional[StrictBool] = None
    memory_text: Optional[StrictStr] = Field(None, alias="memoryText")
    __properties = ["enabled", "memoryText"]

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
    def from_json(cls, json_str: str) -> KVMemoryConfig:
        """Create an instance of KVMemoryConfig from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> KVMemoryConfig:
        """Create an instance of KVMemoryConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return KVMemoryConfig.parse_obj(obj)

        _obj = KVMemoryConfig.parse_obj({
            "enabled": obj.get("enabled"),
            "memory_text": obj.get("memoryText")
        })
        return _obj

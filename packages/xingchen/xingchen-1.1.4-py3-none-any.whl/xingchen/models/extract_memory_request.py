from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, conlist

from xingchen.models import Message, ModelParameters
from xingchen.models.kv_memory_config import KVMemoryConfig


class ExtractMemoryRequest(BaseModel):
    messages: Optional[conlist(Message, min_items=1)] = Field(...)
    kv_memory_configs: Optional[conlist(KVMemoryConfig)] = Field(None, alias="kvMemoryConfigs")
    model_parameter: Optional[ModelParameters] = Field(None, alias="modelParameter")
    __properties = ["messages", "kvMemoryConfigs", "modelParameter"]

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
    def from_json(cls, json_str: str) -> ExtractMemoryRequest:
        """Create an instance of ExtractMemoryRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExtractMemoryRequest:
        """Create an instance of ExtractMemoryRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExtractMemoryRequest.parse_obj(obj)

        _obj = ExtractMemoryRequest.parse_obj({
            "messages": [Message.from_dict(_item) for _item in obj.get("messages")] if obj.get(
                "messages") is not None else None,
            "kv_memory_configs": [KVMemoryConfig.from_dict(_item) for _item in obj.get("kvMemoryConfigs")] if obj.get(
                "kvMemoryConfigs") is not None else None,
            "model_parameter": ModelParameters.from_dict(obj.get("modelParameter")) if obj.get(
                "modelParameter") is not None else None
        })
        return _obj

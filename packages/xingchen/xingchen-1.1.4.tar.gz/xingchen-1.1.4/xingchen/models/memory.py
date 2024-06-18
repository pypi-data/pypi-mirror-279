from __future__ import annotations

import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, conlist

from xingchen.models.message import Message
from xingchen.models.extract_data import ExtractData


class Memory(BaseModel):
    summaries: Optional[conlist(StrictStr)] = Field(None, alias="summaries")
    originals: Optional[conlist(Message)] = Field(None, alias="originals")
    tags: Optional[conlist(ExtractData)] = Field(None, alias="tags")
    __properties = ["summaries", "originals", "tags"]

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
    def from_json(cls, json_str: str) -> Memory:
        """Create an instance of Memory from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Memory:
        """Create an instance of Memory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Memory.parse_obj(obj)

        _obj = Memory.parse_obj({
            "summaries": obj.get("summaries"),
            "originals": [Message.from_dict(_item) for _item in obj.get("originals")] if obj.get(
                "originals") is not None else None,
            "tags": [ExtractData.from_dict(_item) for _item in obj.get("tags")] if obj.get(
                "tags") is not None else None
        })
        return _obj

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, StrictStr


class StopChatRequest(BaseModel):
    request_id: Optional[StrictStr] = Field(None, alias="requestId")
    content: Optional[StrictStr] = None
    __properties = ["requestId", "content"]

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
    def from_json(cls, json_str: str) -> StopChatRequest:
        """Create an instance of StopChatRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StopChatRequest:
        """Create an instance of StopChatRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StopChatRequest.parse_obj(obj)

        _obj = StopChatRequest.parse_obj({
            "request_id": obj.get("requestId"),
            "content": obj.get("content")
        })
        return _obj

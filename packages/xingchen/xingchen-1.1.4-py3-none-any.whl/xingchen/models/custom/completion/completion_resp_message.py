from __future__ import annotations

import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, conlist
from xingchen.models.custom.completion.completion_resp_tool import AcARespTool


class AcARespMessage(BaseModel):
    """
    Message
    """
    name: Optional[StrictStr] = Field(None, description="角色名称")
    role: StrictStr = Field(None, description="assistant-助手消息")
    content: Optional[StrictStr] = Field(None, description="消息内容")
    tool_calls: Optional[conlist(AcARespTool)] = Field(None, description="工具调用结果")

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
    def from_json(cls, json_str: str) -> AcARespMessage:
        """Create an instance of Message from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)

    @classmethod
    def from_dict(cls, obj: dict) -> AcARespMessage:
        """Create an instance of Message from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            "name": obj.get("name"),
            "role": obj.get("role"),
            "content": obj.get("content"),
            "tool_calls": [AcARespTool.from_dict(v) for v in obj.get("tool_calls", [])]
        })
        return _obj

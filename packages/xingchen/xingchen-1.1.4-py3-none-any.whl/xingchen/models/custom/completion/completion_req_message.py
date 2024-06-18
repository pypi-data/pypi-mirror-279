from __future__ import annotations

import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictStr


class AcAReqMessage(BaseModel):
    """
    Message
    """
    name: Optional[StrictStr] = Field(None, description="角色名称")
    role: StrictStr = Field(...,
                            description="角色类型, user-用户发送的内容；system-系统指令；assistant-助手消息；tool-工具类消息")
    content: Optional[StrictStr] = Field(None, description="消息内容")
    tool_call_id: Optional[StrictStr] = Field(None, description="模型生成的工具调用id")

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
    def from_json(cls, json_str: str) -> AcAReqMessage:
        """Create an instance of Message from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)

    @classmethod
    def from_dict(cls, obj: dict) -> AcAReqMessage:
        """Create an instance of Message from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            "name": obj.get("name"),
            "role": obj.get("role"),
            "content": obj.get("content"),
            "tool_call_id": obj.get("tool_call_id")
        })
        return _obj

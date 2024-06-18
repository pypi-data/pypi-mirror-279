# coding: utf-8

import json
from typing import Optional

from pydantic import BaseModel, Field, StrictStr


class GroupChatReplySetting(BaseModel):
    bot_name: StrictStr = Field(..., alias="botName", description="回复角色名称，必须为群聊角色中的一名角色")
    thought: Optional[StrictStr] = Field(None, alias="thought", description="希望角色如何回复")

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        # 直接使用 json.dumps 序列化，提高性能效率
        return json.dumps(self.dict(by_alias=True, exclude_none=True), indent=4)

    def to_json(self) -> str:
        # 同样，直接序列化，避免不必要的中间步骤
        return json.dumps(self.dict(by_alias=True, exclude_none=True))

    @classmethod
    def from_json(cls, json_str: str) -> 'GroupChatReplySetting':
        # 增加异常处理来确保输入的 JSON 字符串是有效的
        try:
            obj_dict = json.loads(json_str)
            return cls.from_dict(obj_dict)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string")

    def to_dict(self):
        # 简化了代码风格
        return self.dict(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: dict) -> 'GroupChatReplySetting':
        # 移除了对 `obj` 是否为 `None` 的判断，因为 `parse_obj` 已经能够处理 `None` 的情况
        # 同时，明确使用 `cls.__init__` 来创建实例，提高代码的可维护性和健壮性
        if not isinstance(obj, dict):
            raise TypeError("Expected a dictionary object")

        return cls(bot_name=obj.get("botName"), thought=obj.get("thought"))
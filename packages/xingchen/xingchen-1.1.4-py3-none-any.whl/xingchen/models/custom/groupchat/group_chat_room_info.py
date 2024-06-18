# coding: utf-8

import json
from typing import Optional

from pydantic import BaseModel, Field, StrictStr


class GroupChatRoomInfo(BaseModel):
    """
    群聊室信息
    """
    name: StrictStr = Field(..., alias="name", description="群聊室名称")
    description: Optional[StrictStr] = Field(None, alias="description", description="群聊室描述")

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return json.dumps(self.dict(by_alias=True, exlude_none=True), indent=4)

    def to_json(self) -> str:
        return json.dumps(self.dict(by_alias=True, exclude_none=True))

    def to_dict(self):
        return self.dict(by_alias=True, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> 'GroupChatRoomInfo':
        try:
            obj_dict = json.loads(json_str)
            return cls.from_json(obj_dict)
        except json.JSONDecodeError:
            raise ValueError("The input string is not a valid JSON string")

    @classmethod
    def from_dict(cls, obj: dict) -> 'GroupChatRoomInfo':
        if not isinstance(obj, dict):
            raise TypeError("The input object is not a dict")
        return cls(name=obj.get("name"), description=obj.get("description"))

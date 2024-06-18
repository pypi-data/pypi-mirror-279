# coding: utf-8


from __future__ import annotations

import json
import pprint

from pydantic import BaseModel, Field, StrictStr, StrictBool
from typing import Optional


class PlatformPublishConfig(BaseModel):
    """
    平台发布配置
    """
    enabled: Optional[StrictBool] = Field(..., alias="enabled", description="是否开启")
    private_share_type: StrictStr = Field(..., alias="privateShareType", description="""
     私密分享类型
     * selfShare - 仅自己可与角色聊天 （permConfig.allowChat=0）
     * linkShare - 通过链接分享（允许获得链接的星尘用户可与ta聊天）  （permConfig.allowChat=0）
     * allShare  - 所有星尘用户可见（需要平台审核）  （permConfig.allowChat=1）
    """)
    __properties = ["enabled", "privateShareType"]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PlatformPublishConfig:
        """Create an instance of SysReminderRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PlatformPublishConfig:
        """Create an instance of SysReminderRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PlatformPublishConfig.parse_obj(obj)

        _obj = PlatformPublishConfig.parse_obj({
            "enabled": obj.get("enabled"),
            "private_share_type": obj.get("privateShareType")
        })
        return _obj



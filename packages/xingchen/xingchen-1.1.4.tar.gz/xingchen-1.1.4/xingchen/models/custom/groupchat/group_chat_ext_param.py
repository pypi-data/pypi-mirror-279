# coding: utf-8

import json

from pydantic import BaseModel, Field, conlist

from xingchen.models.character_key import CharacterKey
from xingchen.models.custom.groupchat.group_chat_reply_setting import GroupChatReplySetting
from xingchen.models.custom.groupchat.group_chat_room_info import GroupChatRoomInfo
from xingchen.models.user_profile import UserProfile


class GroupChatExtParam(BaseModel):
    """
    GroupChatExtParam
    """
    bot_profiles: conlist(CharacterKey, max_items=10, min_items=1) = Field(..., alias="botProfiles",
                                                                           description="群聊角色定义")
    reply_setting: GroupChatReplySetting = Field(None, alias="replySetting", description="回复设置")
    user_profile: UserProfile = Field(..., alias="userProfile", description="用户角色定义")
    group_info: GroupChatRoomInfo = Field(..., alias="groupInfo", description="群聊信息")
    __properties = ["botProfiles", "replySetting", "userProfile", "groupInfo"]

    def to_str(self) -> str:
        # 直接使用 json.dumps 序列化，提高性能效率
        return json.dumps(self.dict(by_alias=True, exclude_none=True), indent=4)

    def to_json(self) -> str:
        # 同样，直接序列化，避免不必要的中间步骤
        return json.dumps(self.dict(by_alias=True, exclude_none=True))

    def to_dict(self):
        # 简化了代码风格
        return self.dict(by_alias=True, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> 'GroupChatExtParam':
        # 增加异常处理来确保输入的 JSON 字符串是有效的
        try:
            obj_dict = json.loads(json_str)
            return cls.from_dict(obj_dict)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string")

    @classmethod
    def from_dict(cls, obj: dict) -> 'GroupChatExtParam':
        # 移除了对 `obj` 是否为 `None` 的判断，因为 `parse_obj` 已经能够处理 `None` 的情况
        # 同时，明确使用 `cls.__init__` 来创建实例，提高代码的可维护性和健壮性
        if not isinstance(obj, dict):
            raise TypeError("Expected a dictionary object")

        return cls(
            bot_profiles=CharacterKey.from_dict(obj.get("botProfiles")) if obj.get(
                "botProfiles") is not None else None,
            reply_setting=GroupChatReplySetting.from_dict(obj.get("replySetting")) if obj.get(
                "replySetting") is not None else None,
            user_profile=UserProfile.from_dict(obj.get("userProfile")) if obj.get("userProfile") is not None else None,
            group_info=GroupChatRoomInfo.from_dict(obj.get("groupInfo")) if obj.get("groupInfo") is not None else None

        )

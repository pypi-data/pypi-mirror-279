# coding: utf-8


from __future__ import annotations

import json
import pprint
from typing import Optional, Any

from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, StrictInt

from xingchen.models.long_term_memory import LongTermMemory
from xingchen.models.repository_info import RepositoryInfo
from xingchen.models.custom.character_model_parameters import CharacterModelParameters


class CharacterAdvancedConfig(BaseModel):
    """
    角色高级配置
    """
    repository_info: Optional[RepositoryInfo] = Field(None, alias="repositoryInfo")
    is_real_info: Optional[StrictBool] = Field(None, alias="isRealInfo", description="是否返回真实世界信息")
    search_keyword: Optional[StrictStr] = Field(None, alias="searchKeyword", description="web搜索必填关键字")
    allow_send_image: Optional[StrictBool] = Field(None, alias="allowSendImage", description="是否允许角色发送图片")
    image_style: Optional[StrictStr] = Field(None, alias="imageStyle", description="角色发送图片的风格")
    allow_send_asr: Optional[StrictBool] = Field(None, alias="allowSendAsr", description="是否允许角色发送语音")
    asr_style: Optional[StrictStr] = Field(None, alias="asrStyle", description="角色发送语音风格")
    chat_description: Optional[StrictStr] = Field(None, alias="chatDescription", description="对话介绍")
    is_real_time: Optional[StrictBool] = Field(None, alias="isRealTime", description="是否获取真实时间")
    short_term_memory_round: Optional[StrictInt] = Field(None, alias="shortTermMemoryRound", description="""
    短期记忆轮数，若使用平台对话历史，可以通过该参数获取指定轮数的对话历史作为短期记忆，超过该轮数，会到长期记忆库中搜索用户query相关问题答案
    """)
    long_term_memories: Optional[conlist(LongTermMemory)] = Field(None, alias="longTermMemories",
                                                                  description="打开长期记忆设置")
    platform_plugins: Optional[conlist(Any)] = Field(None, alias="platformPlugins", description="平台插件")
    knowledge_bases: Optional[conlist(StrictStr)] = Field(None, alias="knowledgeBases", description="知识库")
    __properties = ["repositoryInfo", "isRealInfo", "searchKeyword", "allowSendImage", "imageStyle", "allowSendAsr",
                    "asrStyle", "chatDescription", "shortTermMemoryRound", "longTermMemories", "platformPlugins",
                    "knowledgeBases"]

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
    def from_json(cls, json_str: str) -> CharacterAdvancedConfig:
        """Create an instance of CharacterAdvancedConfig from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of repository_info
        if self.repository_info:
            _dict['repositoryInfo'] = self.repository_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CharacterAdvancedConfig:
        """Create an instance of CharacterAdvancedConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CharacterAdvancedConfig.parse_obj(obj)

        _obj = CharacterAdvancedConfig.parse_obj({
            "repository_info": RepositoryInfo.from_dict(obj.get("repositoryInfo")) if obj.get(
                "repositoryInfo") is not None else None,
            "is_real_info": obj.get("isRealInfo"),
            "search_keyword": obj.get("searchKeyword"),
            "allow_send_image": obj.get("allowSendImage"),
            "image_style": obj.get("imageStyle"),
            "allow_send_asr": obj.get("allowSendAsr"),
            "asr_style": obj.get("asrStyle"),
            "chat_description": obj.get("chatDescription"),
            "is_real_time": obj.get("isRealTime"),
            "short_term_memory_round": obj.get("shortTermMemoryRound"),
            "long_term_memories": [LongTermMemory.from_dict(_item) for _item in obj.get("longTermMemories")] if obj.get(
                "longTermMemories") is not None else None,
            "platform_plugins": obj.get("platformPlugins"),
            "knowledge_bases": obj.get("knowledgeBases")
        })
        return _obj

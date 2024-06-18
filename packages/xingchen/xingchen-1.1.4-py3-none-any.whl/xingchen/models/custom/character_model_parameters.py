# coding: utf-8

"""
角色模型参数配置
"""


from __future__ import annotations

import json
import pprint
from typing import Optional, Union

from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr


class CharacterModelParameters(BaseModel):
    """
    ModelParameters
    """
    chat_model: Optional[StrictStr] = Field(None, alias="chatModel")
    top_p: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="topP")
    max_length: Optional[StrictInt] = Field(None, alias="maxLength")
    min_length: Optional[StrictInt] = Field(None, alias="minLength")
    temperature: Optional[Union[StrictFloat, StrictInt]] = None

    __properties = ["chatModel", "topP", "maxLength", "minLength", "temperature"]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CharacterModelParameters:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CharacterModelParameters:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CharacterModelParameters.parse_obj(obj)

        _obj = CharacterModelParameters.parse_obj({
            "chat_model": obj.get("chatModel"),
            "top_p": obj.get("topP"),
            "max_length": obj.get("maxLength"),
            "min_length": obj.get("minLength"),
            "temperature": obj.get("temperature")
        })
        return _obj



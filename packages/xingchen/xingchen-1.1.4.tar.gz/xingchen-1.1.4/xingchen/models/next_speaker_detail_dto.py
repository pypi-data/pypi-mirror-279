from __future__ import annotations

import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictStr

from xingchen.models import Context
from xingchen.models.custom import Usage


class NextSpeakerDetailDTO(BaseModel):
    name: Optional[StrictStr] = Field(None, alias="name")
    thought: Optional[StrictStr] = Field(None, alias="thought")
    usage: Optional[Usage] = Field(None, alias="usage")
    context: Optional[Context] = Field(None, alias="context")
    __properties = ["name", "thought", "usage", "context"]

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
    def from_json(cls, json_str: str) -> NextSpeakerDetailDTO:
        """Create an instance of NextSpeakerDetailDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> NextSpeakerDetailDTO:
        """Create an instance of NextSpeakerDetailDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return NextSpeakerDetailDTO.parse_obj(obj)

        _obj = NextSpeakerDetailDTO.parse_obj({
            "name": obj.get("name"),
            "thought": obj.get("thought"),
            "usage": Usage.from_dict(obj.get("usage")) if obj.get("usage") is not None else None,
            "context": Context.from_dict(obj.get("context")) if obj.get("context") is not None else None
        })
        return _obj

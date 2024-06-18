from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import Field, StrictStr

from xingchen.models.platform_plugin import PlatformPlugin
from xingchen.models.reject_condition import RejectCondition


class TextToImagePlugin(PlatformPlugin):
    image_style: Optional[StrictStr] = Field(None, alias="imageStyle", description="图片风格")
    positive_desc: Optional[StrictStr] = Field(None, alias="positiveDesc", description="正向描述")
    negative_desc: Optional[StrictStr] = Field(None, alias="negativeDesc", description="负向描述")
    __properties = ["imageStyle", "positiveDesc", "negativeDesc"]

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
    def from_json(cls, json_str: str) -> TextToImagePlugin:
        """Create an instance of TextToImagePlugin from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TextToImagePlugin:
        """Create an instance of TextToImagePlugin from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PlatformPlugin.parse_obj(obj)

        _obj = TextToImagePlugin.parse_obj({
            "enabled": obj.get("enabled"),
            "name": obj.get("name"),
            "image_style": obj.get("imageStyle"),
            "positive_desc": obj.get("positiveDesc"),
            "negative_desc": obj.get("negativeDesc")
        })
        return _obj

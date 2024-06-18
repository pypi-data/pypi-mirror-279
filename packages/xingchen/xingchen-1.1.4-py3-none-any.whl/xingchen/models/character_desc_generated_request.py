from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, StrictStr

from xingchen.models.model_parameters import ModelParameters


class CharacterDescGeneratedRequest(BaseModel):
    type: Optional[StrictStr] = Field(None, alias="type")
    file_url: Optional[StrictStr] = Field(None, alias="fileUrl")
    text: Optional[StrictStr] = Field(None, alias="text")
    file_name: Optional[StrictStr] = Field(None, alias="fileName")
    model_parameter: Optional[ModelParameters] = Field(None, alias="modelParameter")
    __properties = ["type", "fileUrl", "text", "fileName", "modelParameter"]

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
    def from_json(cls, json_str: str) -> CharacterDescGeneratedRequest:
        """Create an instance of CharacterDescGeneratedRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CharacterDescGeneratedRequest:
        """Create an instance of CharacterDescGeneratedRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CharacterDescGeneratedRequest.parse_obj(obj)

        _obj = CharacterDescGeneratedRequest.parse_obj({
            "type": obj.get("type"),
            "file_url": obj.get("fileUrl"),
            "text": obj.get("text"),
            "file_name": obj.get("fileName"),
            "model_parameter": ModelParameters.from_dict(obj.get("modelParameter")) if obj.get(
                "modelParameter") is not None else None
        })
        return _obj

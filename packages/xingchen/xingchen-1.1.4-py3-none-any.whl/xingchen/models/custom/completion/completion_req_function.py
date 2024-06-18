import json
import pprint
from typing import Dict

from pydantic import BaseModel, Field


class AcAReqFunction(BaseModel):
    """
    completions 接口请求参数
    """
    name: str = Field(..., title="function名", description="function名")
    description: str = Field(..., title="function描述", description="function描述")
    parameters: Dict = Field(..., title="function参数定义", description="function参数定义，json schema格式")

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
    def from_json(cls, json_str: str) -> 'AcAReqFunction':
        """Create an instance of Message from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> 'AcAReqFunction':
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "parameters": obj.get("parameters")
        })
        return _obj
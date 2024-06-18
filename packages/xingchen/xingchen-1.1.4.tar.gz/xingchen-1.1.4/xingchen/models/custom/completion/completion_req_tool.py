import json
import pprint
from typing import Optional

from pydantic import BaseModel, StrictStr, Field

from xingchen import AcAReqFunction


class AcAReqTool(BaseModel):
    id: Optional[StrictStr] = Field(None, description="工具ID")
    type: Optional[StrictStr] = Field(None, description="工具类型, 目前只支持 function")
    function: Optional[AcAReqFunction] = Field(..., description="工具函数")

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
    def from_json(cls, json_str: str) -> 'AcAReqTool':
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
    def from_dict(cls, obj: dict) -> 'AcAReqTool':
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            "id": obj.get("id"),
            "type": obj.get("type"),
            "function": obj.get("function")
        })
        return _obj

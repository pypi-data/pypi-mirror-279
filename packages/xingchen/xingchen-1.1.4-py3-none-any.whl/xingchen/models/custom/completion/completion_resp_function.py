import json
import pprint

from pydantic import BaseModel, Field


class AcARespFunction(BaseModel):
    """
    completions 接口响应函数
    """
    name: str = Field(None, title="function名称", description="function名称")
    arguments: str = Field(None, title="模型输出function参数值", description="模型输出function参数值，json str格式")

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
    def from_json(cls, json_str: str) -> 'AcARespFunction':
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
    def from_dict(cls, obj: dict) -> 'AcARespFunction':
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            "name": obj.get("name"),
            "arguments": obj.get("arguments")
        })
        return _obj

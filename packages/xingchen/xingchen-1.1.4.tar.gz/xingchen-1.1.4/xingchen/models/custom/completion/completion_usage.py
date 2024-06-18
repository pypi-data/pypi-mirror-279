import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictInt


class AcAUsage(BaseModel):
    """
    用量统计
    """
    prompt_tokens: Optional[StrictInt] = Field(None, description="Prompt token 数")
    completion_tokens: Optional[StrictInt] = Field(None, description="模型生成 token 数")
    total_tokens: Optional[StrictInt] = Field(None, description="token总数")

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.dict(by_alias=True))

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the model using alias"""
        return self.dict(by_alias=True, exclude={}, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> 'AcAUsage':
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> 'AcAUsage':
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return AcAUsage.parse_obj(obj)
        return AcAUsage.parse_obj({
            'prompt_tokens': obj.get('prompt_tokens'),
            'completion_tokens': obj.get('completion_tokens'),
            'total_tokens': obj.get('total_tokens')
        })

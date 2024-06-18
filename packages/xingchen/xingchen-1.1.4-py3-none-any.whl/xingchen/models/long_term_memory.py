from __future__ import annotations

import json
import pprint
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, StrictBool, conlist

from xingchen.models.kv_memory_config import KVMemoryConfig


class LongTermMemory(BaseModel):
    enabled: Optional[StrictBool] = Field(None, description="是否启动")
    memory_type: Optional[StrictStr] = Field(None, alias="memoryType", description="记忆类型")
    kv_memory_configs: Optional[conlist(KVMemoryConfig)] = Field(None, alias="kvMemoryConfigs",
                                                                 description="kv记忆配置,当memoryType为kv时生效")
    __properties = ["enabled", "memoryType", "kvMemoryConfigs"]

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
    def from_json(cls, json_str: str) -> LongTermMemory:
        """Create an instance of LongTermMemory from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LongTermMemory:
        """Create an instance of LongTermMemory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return KVMemoryConfig.parse_obj(obj)

        _obj = KVMemoryConfig.parse_obj({
            "enabled": obj.get("enabled"),
            "memory_type": obj.get("memoryType"),
            "kv_memory_configs": [KVMemoryConfig.from_dict(_item) for _item in obj.get("kvMemoryConfigs")] if obj.get(
                "kvMemoryConfigs") is not None else None
        })
        return _obj

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, conlist


class PollingImageDetailDTO(BaseModel):
    task_id: Optional[StrictStr] = Field(None, alias="taskId")
    status: Optional[StrictStr] = None
    error_message: Optional[StrictStr] = Field(None, alias="errorMessage")
    file_url: Optional[conlist(StrictStr)] = Field(None, alias="fileUrl")

    __properties = ["taskId", "status", "errorMessage", "fileUrl"]

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
    def from_json(cls, json_str: str) -> PollingImageDetailDTO:
        """Create an instance of PollingImageDetailDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PollingImageDetailDTO:
        """Create an instance of PollingImageDetailDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PollingImageDetailDTO.parse_obj(obj)

        _obj = PollingImageDetailDTO.parse_obj({
            "task_id": obj.get("taskId"),
            "status": obj.get("status"),
            "error_message": obj.get("errorMessage"),
            "file_url": obj.get("fileUrl")
        })
        return _obj

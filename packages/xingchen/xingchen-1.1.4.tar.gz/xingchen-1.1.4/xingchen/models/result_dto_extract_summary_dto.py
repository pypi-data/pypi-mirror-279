
from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from xingchen.models.extract_summary_dto import ExtractSummaryDTO


class ResultDTOExtractSummaryDTO(BaseModel):
    request_id: Optional[StrictStr] = Field(None, alias="requestId")
    code: Optional[StrictInt] = None
    error_message: Optional[StrictStr] = Field(None, alias="errorMessage")
    error_message_key: Optional[StrictStr] = Field(None, alias="errorMessageKey")
    data: Optional[ExtractSummaryDTO] = None
    success: Optional[StrictBool] = None
    __properties = ["requestId", "code", "errorMessage", "errorMessageKey", "data", "success"]

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
    def from_json(cls, json_str: str) -> ResultDTOExtractSummaryDTO:
        """Create an instance of ResultDTOExtractSummaryDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of data
        if self.data:
            _dict['data'] = self.data.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ResultDTOExtractSummaryDTO:
        """Create an instance of ResultDTOExtractSummaryDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ResultDTOExtractSummaryDTO.parse_obj(obj)

        _obj = ResultDTOExtractSummaryDTO.parse_obj({
            "request_id": obj.get("requestId"),
            "code": obj.get("code"),
            "error_message": obj.get("errorMessage"),
            "error_message_key": obj.get("errorMessageKey"),
            "data": ExtractSummaryDTO.from_dict(obj.get("data")) if obj.get("data") is not None else None,
            "success": obj.get("success")
        })
        return _obj

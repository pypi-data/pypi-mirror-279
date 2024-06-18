import json
import pprint

from pydantic import Field, conlist

from xingchen.models.custom.base_response import BaseResponse
from xingchen.models.custom.completion.completion_choice import AcAChoice
from xingchen.models.custom.completion.completion_usage import AcAUsage


class AcACompletionResp(BaseResponse):
    """
    Completion response
    """
    id: str = Field(None, description="A unique identifier for the chat completion.")
    created: int = Field(None, description="The Unix timestamp (in seconds) of when the chat completion was created.")
    model: str = Field(None, description="The model used for the chat completion.")
    choices: conlist(AcAChoice) = Field(None, description="A list of chat completion choices. Can be more than one if n is greater than 1.")
    usage: AcAUsage = Field(None, description="Usage statistics for the completion request.")

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=False, exclude_none=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'AcACompletionResp':
        """Create an instance of Message from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=False,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> 'AcACompletionResp':
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            'request_id': obj.get('requestId'),
            'error_code': obj.get('errorCode'),
            'error_message': obj.get('errorMessage'),
            'error_name': obj.get('errorName'),
            'http_status_code': obj.get('httpStatusCode'),
            'code': obj.get('code'),
            'error_message_key': obj.get('errorMessageKey'),
            'success': obj.get('success'),
            "id": obj.get("id"),
            "created": obj.get("created"),
            "model": obj.get("model"),
            "choices": [AcAChoice.from_dict(c) for c in obj.get("choices", []) if c is not None],
            "usage": obj.get("usage"),
        })
        return _obj

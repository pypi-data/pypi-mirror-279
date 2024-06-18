import json
import pprint
from typing import Dict, Optional, Any

from pydantic import BaseModel, Field, conlist, StrictStr, StrictFloat, StrictInt, StrictBool

from xingchen import AcAReqMessage, AcAReqTool


class AcACompletionReq(BaseModel):
    """
    completions 接口请求参数
    """
    messages: conlist(AcAReqMessage) = Field(..., description="""
    A list of messages comprising the conversation so far.
    Contain system message, user message, assistant message and tool message.
    """)
    model: StrictStr = Field(..., description="""
    xingchen model name, such as xingchen-plus
    """)
    max_tokens: Optional[StrictInt] = Field(None, alias="max_tokens", description="""
    The maximum number of tokens that can be generated in the chat completion.
    """)
    seed: Optional[StrictInt] = Field(None, description="""
    If specified, our system will make a best effort to sample deterministically, 
    such that repeated requests with the same seed and parameters should return the same result. 
    """)
    stream: Optional[StrictBool] = Field(None, description="""
    If set, partial message deltas will be sent,
    Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a event: stop
    """)
    temperature: Optional[StrictFloat] = Field(None, description="""
    Between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    We generally recommend altering this or top_p but not both.
    """)
    top_p: Optional[StrictFloat] = Field(None, description="""
    An alternative to sampling with temperature, called nucleus sampling, 
    where the model considers the results of the tokens with top_p probability mass. 
    So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    """)
    tools: Optional[conlist(AcAReqTool)] = Field(None, description="""
    A list of tools the model may call. Currently, only functions are supported as a tool. 
    Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported.
    """)
    tool_choice: Optional[Any] = Field(None, alias="tool_choice", description="""
    Controls which (if any) tool is called by the model. 
    none means the model will not call any tool and instead generates a message. 
    auto means the model can pick between generating a message or calling one or more tools. 
    required means the model must call one or more tools. 
    Specifying a particular tool via {"type": "function", "function": {"name": "my_function"}} forces the model to call that tool.
    """)
    user: Optional[StrictStr] = Field(..., description="用户标识")

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
    def from_json(cls, json_str: str) -> 'AcACompletionReq':
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
    def from_dict(cls, obj: dict) -> 'AcACompletionReq':
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.parse_obj(obj)

        _obj = cls.parse_obj({
            "messages": obj.get("messages"),
            "model": obj.get("model"),
            "max_tokens": obj.get("max_tokens"),
            "seed": obj.get("seed"),
            "stream": obj.get("stream"),
            "top_p": obj.get("top_p"),
            "tools": obj.get("tools"),
            "tool_choice": obj.get("tool_choice"),
            "user": obj.get("user"),
        })
        return _obj

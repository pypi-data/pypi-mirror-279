# coding: utf-8
from typing import Union, Generator, Any

import requests
from pydantic import Field
from pydantic import validate_arguments
from sseclient import SSEClient
from typing_extensions import Annotated

from xingchen import AcACompletionReq, AcACompletionResp, aca_util
from xingchen.aca_util import handle_completion_sse_response
from xingchen.api_client import ApiClient
from xingchen.exceptions import (
    ApiTypeError
)
from xingchen.models.custom import ChatResponse


class AcACompletionApiSub:
    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    def version(self):
        return self.api_client.api_version()

    @validate_arguments
    def completions(self, chat_req_params: Annotated[AcACompletionReq, Field(..., description="对话请求")],
                    **kwargs) -> Union[AcACompletionResp, Generator[AcACompletionResp, None, None]]:
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the chat_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.chat_with_http_info(chat_req_params, **kwargs)  # noqa: E501

    @validate_arguments
    def chat_with_http_info(self, chat_req_params: Annotated[AcACompletionReq, Field(..., description="对话请求")],
                            **kwargs) -> Union[AcACompletionResp, Generator[AcACompletionResp, None, None]]:  # noqa: E501

        _params = locals()

        _all_params = [
            'chat_req_params'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method chat" % _key
                )
            _params[_key] = _val

        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['chat_req_params'] is not None:
            _body_params = _params['chat_req_params']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/event-stream'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "object",
        }

        # 参数转化
        version = self.version()

        is_stream = 'enable' == _header_params.get('X-DashScope-SSE') or 'enable' == _header_params.get('X-AcA-SSE') \
                    or chat_req_params.stream
        path = '/{0}/api/completions'.format(version)
        host = self.api_client.configuration.host

        _header_params['x-fag-appcode'] = 'aca'
        _header_params['Authorization'] = 'Bearer ' + self.api_client.configuration.access_token

        if is_stream:
            service_name = aca_util.get_service_router(path, True)
            _header_params['Accept'] = 'text/event-stream;charset=UTF-8'
            _header_params['x-fag-servicename'] = service_name

            body_params = self.api_client.sanitize_for_serialization(_body_params)

            request = requests.post(
                host + path,
                headers=_header_params,
                json=body_params,
                stream=True
            )
            client = SSEClient(request)
            return (res for res in handle_completion_sse_response(client))

        response = self.api_client.call_api(
            '/{0}/api/completions'.format(version), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

        d = response
        error_code = d.get('errorCode', None)
        if error_code is not None:
            return ChatResponse.from_dict(d)
        return AcACompletionResp.from_dict(d)

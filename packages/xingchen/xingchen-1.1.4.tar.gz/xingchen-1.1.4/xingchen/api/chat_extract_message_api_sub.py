import re  # noqa: F401

from pydantic import Field
from pydantic import validate_arguments
from typing_extensions import Annotated

from xingchen.api_client import ApiClient
from xingchen.api_response import ApiResponse
from xingchen.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)
from xingchen.models.extract_memory_request import ExtractMemoryRequest
from xingchen.models.result_dto_extract_summary_dto import ResultDTOExtractSummaryDTO


class ChatExtractMessageApiSub:
    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    def version(self):
        return self.api_client.api_version()

    @validate_arguments
    def extract_memory_summary(self, extract_memory_request: Annotated[
        ExtractMemoryRequest, Field(..., description="抽取内容请求")],
                               **kwargs) -> ResultDTOExtractSummaryDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the extract_memory_summary_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.extract_memory_summary_with_http_info(extract_memory_request, **kwargs)  # noqa: E501

    @validate_arguments
    def extract_memory_summary_with_http_info(self, extract_memory_request: Annotated[
        ExtractMemoryRequest, Field(..., description="抽取内容请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'extract_memory_request'
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
                    " to method extract_memory_summary" % _key
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
        if _params['extract_memory_request'] is not None:
            _body_params = _params['extract_memory_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOExtractSummaryDTO",
        }

        return self.api_client.call_api(
            '/{0}/api/extract/summary'.format(self.version()), 'POST',
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

    @validate_arguments
    def extract_memory_kv(self,
                          extract_memory_request: Annotated[ExtractMemoryRequest, Field(..., description="抽取内容请求")],
                          **kwargs) -> ResultDTOExtractSummaryDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the extract_memory_kv_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.extract_memory_kv_with_http_info(extract_memory_request, **kwargs)  # noqa: E501

    @validate_arguments
    def extract_memory_kv_with_http_info(self, extract_memory_request: Annotated[
        ExtractMemoryRequest, Field(..., description="抽取内容请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'extract_memory_request'
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
                    " to method extract_memory_kv" % _key
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
        if _params['extract_memory_request'] is not None:
            _body_params = _params['extract_memory_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOExtractKVDTO",
        }

        return self.api_client.call_api(
            '/{0}/api/extract/kv'.format(self.version()), 'POST',
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

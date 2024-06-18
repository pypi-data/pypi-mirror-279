import re  # noqa: F401

from pydantic import Field, StrictInt
from pydantic import validate_arguments
from typing_extensions import Annotated

from xingchen.api_client import ApiClient
from xingchen.api_response import ApiResponse
from xingchen.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)
from xingchen.models.file_conver_request import FileConvertRequest
from xingchen.models.result_dto_file_conver_dto import ResultDTOFileConvertDTO


class CommonApiSub:
    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    def version(self):
        return self.api_client.api_version()

    @validate_arguments
    def file_convert(self, file_convert_request: Annotated[
        FileConvertRequest, Field(..., description="文件格式转换请求")],
                     **kwargs) -> ResultDTOFileConvertDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the file_convert_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.file_convert_with_http_info(file_convert_request, **kwargs)  # noqa: E501

    @validate_arguments
    def file_convert_with_http_info(self, file_convert_request: Annotated[
        FileConvertRequest, Field(..., description="文件格式转换请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'file_convert_request'
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
                    " to method file_convert" % _key
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
        if _params['file_convert_request'] is not None:
            _body_params = _params['file_convert_request']

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
            '200': "ResultDTOFileConvertDTO",
        }

        return self.api_client.call_api(
            '/{0}/api/common/file/asyn/upload'.format(self.version()), 'POST',
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
    def file_convert_result(self, task_id: Annotated[StrictInt, Field(..., description="任务ID")],
                            **kwargs) -> ResultDTOFileConvertDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the file_convert_result_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.file_convert_result_with_http_info(task_id, **kwargs)  # noqa: E501

    @validate_arguments
    def file_convert_result_with_http_info(self, task_id: Annotated[StrictInt, Field(..., description="任务ID")],
                                           **kwargs) -> ApiResponse:  # noqa: E501
        _params = locals()

        _all_params = [
            'task_id'
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
                    " to method file_convert_result" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('task_id') is not None:  # noqa: E501
            _query_params.append(('taskId', _params['task_id']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOFileConvertDTO",
        }

        return self.api_client.call_api(
            '/{api_version}/api/common/file/asyn/download'.format(
                api_version=self.api_client.configuration.api_version), 'GET',
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

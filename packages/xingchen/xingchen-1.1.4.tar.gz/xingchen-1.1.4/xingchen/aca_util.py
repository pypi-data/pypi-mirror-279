from typing import List

from xingchen.models import ChatReqParams, BaseChatRequest, Input
from xingchen.models.custom import ChatResponse, ChatResult
from xingchen.models.custom.completion.completion_resp import AcACompletionResp
from xingchen.models.platform_plugin import PlatformPlugin
from xingchen.models.reject_answer_plugin import RejectAnswerPlugin
from xingchen.models.text_to_image_plugin import TextToImagePlugin
from sseclient import SSEClient
import json

api_router_map = {
    '/v2/api/chat/send': 'aca-chat-send',
    '/v2/api/groupchat/send': 'aca-groupchat-send',
    '/v2/api/character/create': 'aca-character-create',
    '/v2/api/character/update': 'aca-character-update',
    '/v2/api/character/details': 'aca-character-details',
    '/v2/api/character/delete': 'aca-character-delete',
    '/v2/api/character/search': 'aca-character-search',
    '/v2/api/character/createOrUpdateVersion': 'aca-character-version-mgmt',
    '/v2/api/character/versions': 'aca-character-versions',
    '/v2/api/character/newversion/recommend': 'aca-character-version-recommend',
    '/v2/api/chat/message/histories': 'aca-message-history',
    '/v2/api/chat/rating': 'aca-message-rating',
    '/v2/api/chat/reminder': 'aca-chat-reminder',
    '/v2/api/chat/reset': 'aca-chat-reset',
    '/v2/api/extract/kv': 'aca-extract-memory-kv',
    '/v2/api/extract/summary': 'aca-extract-memory-summary',
    '/v2/api/character/auto/desc': 'aca-char-auto-desc',
    '/v2/api/chat/polling/image': 'aca-polling-image',
    '/v2/api/chat/stop': 'aca-chat-stop',
    '/v2/api/common/file/asyn/upload': 'aca-doc-converter-submit',
    '/v2/api/common/file/asyn/download': 'aca-doc-converter-result',
    '/v2/api/completions': 'aca-completion',
    '/v2/api/groupchat/nextSpeaker': 'aca-groupchat-nextspeaker'
}


def get_service_router(path, async_req):
    if not path:
        return None
    if path.__eq__('/v2/api/chat/send') and async_req:
        return 'aca-chat-send-sse'
    if path.__eq__('/v2/api/groupchat/send') and async_req:
        return 'aca-groupchat-send-sse'
    return api_router_map.get(path)


def convert_chat_params(chat_req_params: ChatReqParams):
    bot_profile = chat_req_params.bot_profile
    parameters = chat_req_params.model_parameters
    user_profile = chat_req_params.user_profile
    scenario = chat_req_params.scenario
    messages = chat_req_params.messages
    sample_messages = chat_req_params.sample_messages
    model_name = parameters.model_name if parameters is not None else None
    functions = chat_req_params.functions
    plugins = chat_req_params.plugins
    function_choice = chat_req_params.function_choice
    context = chat_req_params.context
    memory = chat_req_params.memory
    advanced_settings = chat_req_params.advanced_settings
    platform_plugins = chat_req_params.platform_plugins
    pre_check_plugin_process(platform_plugins)
    aca = {
        'botProfile': bot_profile,
        'userProfile': user_profile,
        'sampleMessages': sample_messages,
        'scenario': scenario,
        'functionList': functions,
        'pluginList': plugins,
        'functionChoice': function_choice,
        'context': context,
        'memory': memory,
        "advancedSettings": advanced_settings,
        "platformPlugins": platform_plugins
    }

    return BaseChatRequest(
        model=model_name,
        input=Input(
            prompt='|<system>|',
            messages=messages,
            aca=aca
        ),
        parameters=parameters
    )


def pre_check_plugin_process(platform_plugins: List[PlatformPlugin]):
    if platform_plugins is None or len(platform_plugins) == 0:
        return
    for platform_plugin in platform_plugins:
        if isinstance(platform_plugin, TextToImagePlugin):
            platform_plugin.enabled = False if platform_plugin.enabled is None else platform_plugin.enabled
            if not platform_plugin.name:
                platform_plugin.name = "text_to_image_plugin"
            continue
        if isinstance(platform_plugin, RejectAnswerPlugin):
            platform_plugin.enabled = False if platform_plugin.enabled is None else platform_plugin.enabled
            if not platform_plugin.name:
                platform_plugin.name = "reject_answer_plugin"
            continue
        raise TypeError("Wrong plugin class type")


def handle_sse_response(client: SSEClient):
    events = client.events()
    for event in events:
        d = json.loads(event.data)
        error_code = d.get('errorCode', None)
        if error_code is not None:
            yield ChatResponse.from_dict(d)
            return
        yield ChatResponse(
            success=True,
            http_status_code=200,
            code=200,
            data=ChatResult.from_dict(d)
        )


def handle_completion_sse_response(client: SSEClient):
    events = client.events()
    for event in events:
        d = json.loads(event.data)
        error_code = d.get('errorCode', None)
        if error_code is not None:
            yield ChatResponse.from_dict(d)
            return
        yield AcACompletionResp.from_dict(d)

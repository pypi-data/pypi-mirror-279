import unittest

from xingchen import Configuration, ApiClient, ChatApiSub, ChatReqParams, CharacterKey, Message, UserProfile, ChatContext, Function,\
    ModelParameters


def build_chat_param():
    return ChatReqParams(
        bot_profile=CharacterKey(
            character_id="40f70d5466e1429ba9aa755842b35d9f",
            version=1
        ),
        model_parameters=ModelParameters(
            seed=1683806810,
            incrementalOutput=False,
            model_name="xingchen-plus"
        ),
        messages=[
            Message(
                name='小明',
                role='user',
                content='杭州今天天气怎么样'
            )
        ],
        context=ChatContext(
            use_chat_history=True
        ),
        user_profile=UserProfile(
            user_id='123456789',
            user_name='小明'
        ),
        functions=[
            Function(
                name='weather',
                description='通过调用天气预报API获取当地天气预报信息通过调用天气预报API获取当地天气预报信息',
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "地点"
                        },
                        "format": {
                            "type": "string",
                            "enum": [
                                "celsius",
                                "fahrenheit"
                            ],
                            "description": "温度单位"
                        }
                    },
                }
            )
        ]
    )


class Test(unittest.TestCase):

    @staticmethod
    def init_client():
        configuration = Configuration(
            host="https://nlp.aliyuncs.com"
        )
        configuration.access_token = "lm-OD6MqVvPk32rah/oaeEYpA=="
        with ApiClient(configuration) as api_client:
            api_client.set_default_header("", "")
            api_instance = ChatApiSub(api_client)
        return api_instance

    def test_chat_sync(self):
        api = self.init_client()

        chat_param = build_chat_param()
        res = api.chat(
            chat_req_params=chat_param
        )
        print(res.to_str())
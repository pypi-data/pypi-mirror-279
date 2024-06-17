'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Chat Bot Get User Sessions Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ChatBotGetUserSessionsService(SoffosAIService):
    '''
    Get user sessions
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.CHAT_BOT_GET_USER_SESSIONS
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, chatbot_id:str, user_id:str, engine:str=None, session_ids:list=None) -> dict:
        '''
        Call the Chat Bot Get User Sessions Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param chatbot_id: The chatbot's id.
        :param user_id: A unique user id. It is recommended that your provide a UUID.
        :param engine: The LLM engine to be used.
        :param session_ids: Specify the id of the sessions you need to get.
        :return: engine: The LLM engine used.
        sessions: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat_bot_get_user_sessions.py>`_
        '''
        return super().__call__(user=user, chatbot_id=chatbot_id, user_id=user_id, engine=engine, session_ids=session_ids)

    def set_input_configs(self, name:str, chatbot_id:Union[str, InputConfig], user_id:Union[str, InputConfig], engine:Union[str, InputConfig]=None, session_ids:Union[list, InputConfig]=None):
        super().set_input_configs(name=name, chatbot_id=chatbot_id, user_id=user_id, engine=engine, session_ids=session_ids)

    @classmethod
    def call(self, user:str, chatbot_id:str, user_id:str, engine:str=None, session_ids:list=None) -> dict:
        '''
        Call the Chat Bot Get User Sessions Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param chatbot_id: The chatbot's id.
        :param user_id: A unique user id. It is recommended that your provide a UUID.
        :param engine: The LLM engine to be used.
        :param session_ids: Specify the id of the sessions you need to get.
        :return: engine: The LLM engine used.
        sessions: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat_bot_get_user_sessions.py>`_
        '''
        return super().call(user=user, chatbot_id=chatbot_id, user_id=user_id, engine=engine, session_ids=session_ids)


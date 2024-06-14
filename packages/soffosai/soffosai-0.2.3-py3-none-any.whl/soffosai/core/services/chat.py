'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Chat Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ChatService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.CHAT
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, mode:str, session_id:str=None, engine:str=None, user_id:str=None, message:str=None, messages:list=None, knowledge:str=None, document_ids:list=None) -> dict:
        '''
        Call the Chat Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param mode: None
        :param session_id: None
        :param engine: The LLM engine to be used.
        :param user_id: None
        :param message: None
        :param messages: None
        :param knowledge: None
        :param document_ids: None
        :return: engine: The LLM engine to be used.
        messages: None
        response: None
        session_name: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat.py>`_
        '''
        return super().__call__(user=user, mode=mode, session_id=session_id, engine=engine, user_id=user_id, message=message, messages=messages, knowledge=knowledge, document_ids=document_ids)

    def set_input_configs(self, name:str, mode:Union[str, InputConfig], session_id:Union[str, InputConfig]=None, engine:Union[str, InputConfig]=None, user_id:Union[str, InputConfig]=None, message:Union[str, InputConfig]=None, messages:Union[list, InputConfig]=None, knowledge:Union[str, InputConfig]=None, document_ids:Union[list, InputConfig]=None):
        super().set_input_configs(name=name, mode=mode, session_id=session_id, engine=engine, user_id=user_id, message=message, messages=messages, knowledge=knowledge, document_ids=document_ids)

    @classmethod
    def call(self, user:str, mode:str, session_id:str=None, engine:str=None, user_id:str=None, message:str=None, messages:list=None, knowledge:str=None, document_ids:list=None) -> dict:
        '''
        Call the Chat Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param mode: None
        :param session_id: None
        :param engine: The LLM engine to be used.
        :param user_id: None
        :param message: None
        :param messages: None
        :param knowledge: None
        :param document_ids: None
        :return: engine: The LLM engine to be used.
        messages: None
        response: None
        session_name: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat.py>`_
        '''
        return super().call(user=user, mode=mode, session_id=session_id, engine=engine, user_id=user_id, message=message, messages=messages, knowledge=knowledge, document_ids=document_ids)

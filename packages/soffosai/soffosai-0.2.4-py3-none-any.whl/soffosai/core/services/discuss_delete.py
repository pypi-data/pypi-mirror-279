'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Discuss Delete Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class DiscussDeleteService(SoffosAIService):
    '''
    The Let's Discuss module allows the user to have a conversation with the AI
    about the content provided by the user. The main difference between this module
    and the Question Answering module is that Let's Discuss keeps a history of the
    interactions, allowing it to take in account what was previously discussed when
    generating a response. Unlike Question Answering which is mainly used for
    information retrieval, the Let's Discuss module creates a more natural
    experience similar to having a conversation with a person at the expense of the
    size of the content it can process at a time.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.DISCUSS_DELETE
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, engine:str=None, session_ids:list=None) -> dict:
        '''
        Call the Discuss Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param session_ids: A list with the IDs of the sessions to be deleted.
        :return: engine: The LLM engine used.
        success: Indicates whether the sessions have been successfuly deleted.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/discuss_delete.py>`_
        '''
        return super().__call__(user=user, engine=engine, session_ids=session_ids)

    def set_input_configs(self, name:str, engine:Union[str, InputConfig]=None, session_ids:Union[list, InputConfig]=None):
        super().set_input_configs(name=name, engine=engine, session_ids=session_ids)

    @classmethod
    def call(self, user:str, engine:str=None, session_ids:list=None) -> dict:
        '''
        Call the Discuss Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param session_ids: A list with the IDs of the sessions to be deleted.
        :return: engine: The LLM engine used.
        success: Indicates whether the sessions have been successfuly deleted.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/discuss_delete.py>`_
        '''
        return super().call(user=user, engine=engine, session_ids=session_ids)


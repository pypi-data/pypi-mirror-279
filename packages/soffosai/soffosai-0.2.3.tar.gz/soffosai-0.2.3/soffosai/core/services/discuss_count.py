'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Discuss Count Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class DiscussCountService(SoffosAIService):
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
        service = ServiceString.DISCUSS_COUNT
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, return_messages:bool, engine:str=None) -> dict:
        '''
        Call the Discuss Count Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param return_messages: When set to true, in addition to returning all the session
            records, it will also return all the messages associated with
            each session.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        sessions: List of sessions. Each session contains the following data:
            context: The content discussed in the session. session_id:
            Session's ID. messages: If return_messages is true, this list
            will contain a list of dictionaries representing the
            interactions between the system and the user. Each dictionary
            contains the user's query, the system's response and the
            interaction's ID as message_id, which is an integer indicating
            their order.
        session_count: The count of sessions for your organization. It is important to
            map sessions to your users at the application level.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/discuss_count.py>`_
        '''
        return super().__call__(user=user, return_messages=return_messages, engine=engine)

    def set_input_configs(self, name:str, return_messages:Union[bool, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, return_messages=return_messages, engine=engine)

    @classmethod
    def call(self, user:str, return_messages:bool, engine:str=None) -> dict:
        '''
        Call the Discuss Count Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param return_messages: When set to true, in addition to returning all the session
            records, it will also return all the messages associated with
            each session.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        sessions: List of sessions. Each session contains the following data:
            context: The content discussed in the session. session_id:
            Session's ID. messages: If return_messages is true, this list
            will contain a list of dictionaries representing the
            interactions between the system and the user. Each dictionary
            contains the user's query, the system's response and the
            interaction's ID as message_id, which is an integer indicating
            their order.
        session_count: The count of sessions for your organization. It is important to
            map sessions to your users at the application level.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/discuss_count.py>`_
        '''
        return super().call(user=user, return_messages=return_messages, engine=engine)


'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Chat Bot Create Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ChatBotCreateService(SoffosAIService):
    '''
    Creates a chatbot and returns its ID. The id will later be used to allow users
    to interact with it.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.CHAT_BOT_CREATE
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, role:str, chatbot_name:str, engine:str=None, chatbot_id:str=None) -> dict:
        '''
        Call the Chat Bot Create Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param role: A description of your bot's purpose. You may also describe its
            tone when responding. The system may not be able to follow
            complex instructions specified in this field.
        :param chatbot_name: The name/identity of your chatbot.
        :param engine: The LLM engine to be used.
        :param chatbot_id: The chatbot's id. Provided when you create the chatbot. If you
            provide this, the chatbot with this ID's will be updated. The
            role and name will be updated.
        :return: engine: The LLM engine used.
        chatbot_id: The chatbot's id. Provided when you create the chatbot. If you
            provide this, the chatbot with this ID's will be updated. The
            role and name will be updated.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat_bot_create.py>`_
        '''
        return super().__call__(user=user, role=role, chatbot_name=chatbot_name, engine=engine, chatbot_id=chatbot_id)

    def set_input_configs(self, name:str, role:Union[str, InputConfig], chatbot_name:Union[str, InputConfig], engine:Union[str, InputConfig]=None, chatbot_id:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, role=role, chatbot_name=chatbot_name, engine=engine, chatbot_id=chatbot_id)

    @classmethod
    def call(self, user:str, role:str, chatbot_name:str, engine:str=None, chatbot_id:str=None) -> dict:
        '''
        Call the Chat Bot Create Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param role: A description of your bot's purpose. You may also describe its
            tone when responding. The system may not be able to follow
            complex instructions specified in this field.
        :param chatbot_name: The name/identity of your chatbot.
        :param engine: The LLM engine to be used.
        :param chatbot_id: The chatbot's id. Provided when you create the chatbot. If you
            provide this, the chatbot with this ID's will be updated. The
            role and name will be updated.
        :return: engine: The LLM engine used.
        chatbot_id: The chatbot's id. Provided when you create the chatbot. If you
            provide this, the chatbot with this ID's will be updated. The
            role and name will be updated.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat_bot_create.py>`_
        '''
        return super().call(user=user, role=role, chatbot_name=chatbot_name, engine=engine, chatbot_id=chatbot_id)


'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Chat Bot Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ChatBotService(SoffosAIService):
    '''
    The Chatbot module enables you to create custom chatbots. You can give it a
    name, a purpose and connect it to your document repository so that it informs
    its responses to users from your ingested documents.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.CHAT_BOT
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, message:str, chatbot_id:str, user_id:str, mode:str, session_id:str=None, engine:str=None, previous_messages:list=None, bot_document_ids:list=None, context_document_ids:list=None) -> dict:
        '''
        Call the Chat Bot Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param message: The user's message to the chatbot
        :param chatbot_id: The chatbot's id.
        :param user_id: A unique user id. It is recommended that your provide a UUID.
        :param mode: The value can only be one of: open, closed, hybrid.
        :param session_id: A unique session id for mapping the records to your application.
            It is recommended that you provide a UUID. If not provided, the
            system will not store any information regarding the call and
            will use the value of "previous_messages" as the conversation
            history.
        :param engine: The LLM engine to be used.
        :param previous_messages: This field can be used to provide the conversation history. It
            is ignored if a "session_id" is provided, in which case the
            system will used the stored interactions from that session as
            conversation history.
        :param bot_document_ids: Here you can specify documents that describe the bot's
            background and its perception of itself.
        :param context_document_ids: Pass the ids of the documents that you wish to inform your bot
            with for the specific user/session. Applicable for closed and
            hybrid modes as described above.
        :return: engine: The LLM engine used.
        context_document_ids: Pass the ids of the documents that you wish to inform your bot
            with for the specific user/session. Applicable for closed and
            hybrid modes as described above.
        response: The agent's response
        session_name: The session's name which is generated after 3 interactions.
        messages: A list of the conversation's messages so far.
        context: The context that was made available to the agent for responding
            to the user's last message.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat_bot.py>`_
        '''
        return super().__call__(user=user, message=message, chatbot_id=chatbot_id, user_id=user_id, mode=mode, session_id=session_id, engine=engine, previous_messages=previous_messages, bot_document_ids=bot_document_ids, context_document_ids=context_document_ids)

    def set_input_configs(self, name:str, message:Union[str, InputConfig], chatbot_id:Union[str, InputConfig], user_id:Union[str, InputConfig], mode:Union[str, InputConfig], session_id:Union[str, InputConfig]=None, engine:Union[str, InputConfig]=None, previous_messages:Union[list, InputConfig]=None, bot_document_ids:Union[list, InputConfig]=None, context_document_ids:Union[list, InputConfig]=None):
        super().set_input_configs(name=name, message=message, chatbot_id=chatbot_id, user_id=user_id, mode=mode, session_id=session_id, engine=engine, previous_messages=previous_messages, bot_document_ids=bot_document_ids, context_document_ids=context_document_ids)

    @classmethod
    def call(self, user:str, message:str, chatbot_id:str, user_id:str, mode:str, session_id:str=None, engine:str=None, previous_messages:list=None, bot_document_ids:list=None, context_document_ids:list=None) -> dict:
        '''
        Call the Chat Bot Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param message: The user's message to the chatbot
        :param chatbot_id: The chatbot's id.
        :param user_id: A unique user id. It is recommended that your provide a UUID.
        :param mode: The value can only be one of: open, closed, hybrid.
        :param session_id: A unique session id for mapping the records to your application.
            It is recommended that you provide a UUID. If not provided, the
            system will not store any information regarding the call and
            will use the value of "previous_messages" as the conversation
            history.
        :param engine: The LLM engine to be used.
        :param previous_messages: This field can be used to provide the conversation history. It
            is ignored if a "session_id" is provided, in which case the
            system will used the stored interactions from that session as
            conversation history.
        :param bot_document_ids: Here you can specify documents that describe the bot's
            background and its perception of itself.
        :param context_document_ids: Pass the ids of the documents that you wish to inform your bot
            with for the specific user/session. Applicable for closed and
            hybrid modes as described above.
        :return: engine: The LLM engine used.
        context_document_ids: Pass the ids of the documents that you wish to inform your bot
            with for the specific user/session. Applicable for closed and
            hybrid modes as described above.
        response: The agent's response
        session_name: The session's name which is generated after 3 interactions.
        messages: A list of the conversation's messages so far.
        context: The context that was made available to the agent for responding
            to the user's last message.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/chat_bot.py>`_
        '''
        return super().call(user=user, message=message, chatbot_id=chatbot_id, user_id=user_id, mode=mode, session_id=session_id, engine=engine, previous_messages=previous_messages, bot_document_ids=bot_document_ids, context_document_ids=context_document_ids)


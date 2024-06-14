'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Email Analysis Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class EmailAnalysisService(SoffosAIService):
    '''
    This module extracts key information from the body of an e-mail.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.EMAIL_ANALYSIS
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Email Analysis Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: The e-mail body text.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        analysis: A dictionary containing the following key information: key
            points: string list topics: string list sender: string receiver:
            string list mentions: string list sentiment: string urgency:
            string dates: string list
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/email_analysis.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine)

    @classmethod
    def call(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Email Analysis Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: The e-mail body text.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        analysis: A dictionary containing the following key information: key
            points: string list topics: string list sender: string receiver:
            string list mentions: string list sentiment: string urgency:
            string dates: string list
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/email_analysis.py>`_
        '''
        return super().call(user=user, text=text, engine=engine)


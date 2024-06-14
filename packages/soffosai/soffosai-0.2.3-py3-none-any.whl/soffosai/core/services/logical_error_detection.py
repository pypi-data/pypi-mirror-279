'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Logical Error Detection Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class LogicalErrorDetectionService(SoffosAIService):
    '''
    Identifies illogical statements in text and explains why they are illogical.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.LOGICAL_ERROR_DETECTION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Logical Error Detection Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Input text to analyze for logical errors.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        logical_errors: A list of dictionaries representing detected logical errors.
            Each dictionary contains the following fields: text: The
            illogical text. start: Starting character index in the original
            text. end: Ending chracter index in the original text.
            explanation: The reasoning behind why the text span is
            illogical.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/logical_error_detection.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine)

    @classmethod
    def call(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Logical Error Detection Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Input text to analyze for logical errors.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        logical_errors: A list of dictionaries representing detected logical errors.
            Each dictionary contains the following fields: text: The
            illogical text. start: Starting character index in the original
            text. end: Ending chracter index in the original text.
            explanation: The reasoning behind why the text span is
            illogical.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/logical_error_detection.py>`_
        '''
        return super().call(user=user, text=text, engine=engine)


'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Translation Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TranslationService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TRANSLATION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None, auto_detect:bool=None, source_language_code:str=None, target_language_code:str=None) -> dict:
        '''
        Call the Translation Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: None
        :param engine: The LLM engine to be used.
        :param auto_detect: None
        :param source_language_code: None
        :param target_language_code: None
        :return: engine: The LLM engine used.
        target_language_code: None
        translation: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/translation.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine, auto_detect=auto_detect, source_language_code=source_language_code, target_language_code=target_language_code)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None, auto_detect:Union[bool, InputConfig]=None, source_language_code:Union[str, InputConfig]=None, target_language_code:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine, auto_detect=auto_detect, source_language_code=source_language_code, target_language_code=target_language_code)

    @classmethod
    def call(self, user:str, text:str, engine:str=None, auto_detect:bool=None, source_language_code:str=None, target_language_code:str=None) -> dict:
        '''
        Call the Translation Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: None
        :param engine: The LLM engine to be used.
        :param auto_detect: None
        :param source_language_code: None
        :param target_language_code: None
        :return: engine: The LLM engine used.
        target_language_code: None
        translation: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/translation.py>`_
        '''
        return super().call(user=user, text=text, engine=engine, auto_detect=auto_detect, source_language_code=source_language_code, target_language_code=target_language_code)


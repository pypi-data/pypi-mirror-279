'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Profanity Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ProfanityService(SoffosAIService):
    '''
    Profanity related serializer
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.PROFANITY
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Profanity Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        profanities: List of dictionaries resembling detected profanities. Each
            dictionary contains the following fields: text: The text of the
            profanity. span_start: The starting character index of the
            profanity in the original text. span_end: The ending character
            index of the profanity in the original text.
        offensive_probability: A float value between 0 and 1 indicating the degree of
            offensiveness.
        offensive_prediction: Boolean value indicating whether the probability exceeds the
            threshold of what is definitely considered offensive for the
            underlying model.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/profanity.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine)

    @classmethod
    def call(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Profanity Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        profanities: List of dictionaries resembling detected profanities. Each
            dictionary contains the following fields: text: The text of the
            profanity. span_start: The starting character index of the
            profanity in the original text. span_end: The ending character
            index of the profanity in the original text.
        offensive_probability: A float value between 0 and 1 indicating the degree of
            offensiveness.
        offensive_prediction: Boolean value indicating whether the probability exceeds the
            threshold of what is definitely considered offensive for the
            underlying model.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/profanity.py>`_
        '''
        return super().call(user=user, text=text, engine=engine)


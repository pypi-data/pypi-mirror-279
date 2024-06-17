'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Review Tagger Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ReviewTaggerService(SoffosAIService):
    '''
    This module extracts key information from negative product reviews. It attempts
    to find the referred object, it's fault and an action/verb that is associated
    with it. If any of the information is not present, it returns "n/a". This is
    useful for organizations who want to analyze product reviews in order to
    identify and prioritize the most important issues.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.REVIEW_TAGGER
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Review Tagger Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: The review text.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        object: The faulty object. This could be the product itself, or a
            component, e.g. 'door handle'. If 'n/a' is returned, it's
            assumed that the object is the product itself.
        action: The action/verb associated with that object, e.g. 'squeaks'
        fault: The fault (or strength) of the object, e.g. 'loose' or 'broken'.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/review_tagger.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine)

    @classmethod
    def call(self, user:str, text:str, engine:str=None) -> dict:
        '''
        Call the Review Tagger Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: The review text.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        object: The faulty object. This could be the product itself, or a
            component, e.g. 'door handle'. If 'n/a' is returned, it's
            assumed that the object is the product itself.
        action: The action/verb associated with that object, e.g. 'squeaks'
        fault: The fault (or strength) of the object, e.g. 'loose' or 'broken'.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/review_tagger.py>`_
        '''
        return super().call(user=user, text=text, engine=engine)


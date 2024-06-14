'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use String Similarity Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class StringSimilarityService(SoffosAIService):
    '''
    This module measures the similarity in meaning between two strings. It also
    returns text spans that are similar between the two string, which can be useful
    for highlighting. Although the service accepts srtings up to 5000 characters
    long, it is intended for smaller strings and use-cases such as answer scoring,
    given the correct answer and the learner's answer to a question.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.STRING_SIMILARITY
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, a:str, b:str, engine:str=None) -> dict:
        '''
        Call the String Similarity Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param a: A string to be compared with `b`. Has a limit of 5000 characters.
        :param b: A string to be compared with `a`. Has a limit of 5000 characters.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        score: A value between `0` and `100` indicating the percentage of
            similarity between the two strings. Since the comparison
            assesses the similarity in entailment/meaning, the score will be
            very close to 0, or very close to 100 most of the time. More
            ambiguous cases are scored somewhere in the middle.
        text_spans: A list of dictionaries representing instances where a sub-string
            of `a` is similar to one or more substrings of `b`. Each
            dictionary contains the following fields: a_text_span: A
            dictionary of the span in `a` containing its `text` and `span`
            index offsets. b_text_span: A list of dictionaries of all spans
            similar to `a_text_span`, each containing their `text` and
            `span`.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/string_similarity.py>`_
        '''
        return super().__call__(user=user, a=a, b=b, engine=engine)

    def set_input_configs(self, name:str, a:Union[str, InputConfig], b:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, a=a, b=b, engine=engine)

    @classmethod
    def call(self, user:str, a:str, b:str, engine:str=None) -> dict:
        '''
        Call the String Similarity Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param a: A string to be compared with `b`. Has a limit of 5000 characters.
        :param b: A string to be compared with `a`. Has a limit of 5000 characters.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        score: A value between `0` and `100` indicating the percentage of
            similarity between the two strings. Since the comparison
            assesses the similarity in entailment/meaning, the score will be
            very close to 0, or very close to 100 most of the time. More
            ambiguous cases are scored somewhere in the middle.
        text_spans: A list of dictionaries representing instances where a sub-string
            of `a` is similar to one or more substrings of `b`. Each
            dictionary contains the following fields: a_text_span: A
            dictionary of the span in `a` containing its `text` and `span`
            index offsets. b_text_span: A list of dictionaries of all spans
            similar to `a_text_span`, each containing their `text` and
            `span`.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/string_similarity.py>`_
        '''
        return super().call(user=user, a=a, b=b, engine=engine)


'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Summarization Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class SummarizationService(SoffosAIService):
    '''
    The summarization module utilizes Natural Language Generation (NLG) to generate
    an abstractive summary of a specified length. In contrast to extractive
    summarization methods, which simply calculate the centrality of sentences or
    passages in the original text and concatenate the highest rated ones,
    abstractive summaries are often more concise and accurate. The end result isn't
    necessarily a sum of word-for-word copies of passages from the original text,
    but a combination of all key points formulated as a new text.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.SUMMARIZATION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, sent_length:int, engine:str=None) -> dict:
        '''
        Call the Summarization Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to be summarized.
        :param sent_length: The desired sentence length of the summary. The service will
            respond with a 403 error if the value is larger than the number
            of sentences in the text.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        summary: The summary.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/summarization.py>`_
        '''
        return super().__call__(user=user, text=text, sent_length=sent_length, engine=engine)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], sent_length:Union[int, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, sent_length=sent_length, engine=engine)

    @classmethod
    def call(self, user:str, text:str, sent_length:int, engine:str=None) -> dict:
        '''
        Call the Summarization Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to be summarized.
        :param sent_length: The desired sentence length of the summary. The service will
            respond with a 403 error if the value is larger than the number
            of sentences in the text.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        summary: The summary.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/summarization.py>`_
        '''
        return super().call(user=user, text=text, sent_length=sent_length, engine=engine)


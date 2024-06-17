'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Sentiment Analysis Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class SentimentAnalysisService(SoffosAIService):
    '''
    This module processes the text to measure whether it is negative, positive or
    neutral. The text is processed in segments of user-defined length and it
    provides scores for each segment as well as the overall score of the whole
    text.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.SENTIMENT_ANALYSIS
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None, sentence_split:int=4, sentence_overlap:bool=None) -> dict:
        '''
        Call the Sentiment Analysis Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to be analyzed for sentiment.
        :param engine: The LLM engine to be used.
        :param sentence_split: The number of sentences of each chunk when splitting the input
            text.
        :param sentence_overlap: Whether to overlap adjacent chunks by 1 sentence. For example,
            with sentence_split=3 and sentence_overlap=true: [[s1, s2, s3],
            [s3, s4, s5], [s5, s6, s7]]
        :return: engine: The LLM engine used.
        sentiment_breakdown: A list of dictionaries representing the score of each segment of
            text. Each dictionary contains the following fields: text: The
            text of the segment. start: The starting character index of the
            segment in the original text. end: The ending character index of
            the segment in the original text. sentiment: A dictionary
            containing the scores for negative, neutral and positive.
        sentiment_overall: Contains the overall negative, neutral and positive score for
            the provided text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/sentiment_analysis.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine, sentence_split=sentence_split, sentence_overlap=sentence_overlap)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None, sentence_split:Union[int, InputConfig]=4, sentence_overlap:Union[bool, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine, sentence_split=sentence_split, sentence_overlap=sentence_overlap)

    @classmethod
    def call(self, user:str, text:str, engine:str=None, sentence_split:int=4, sentence_overlap:bool=None) -> dict:
        '''
        Call the Sentiment Analysis Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to be analyzed for sentiment.
        :param engine: The LLM engine to be used.
        :param sentence_split: The number of sentences of each chunk when splitting the input
            text.
        :param sentence_overlap: Whether to overlap adjacent chunks by 1 sentence. For example,
            with sentence_split=3 and sentence_overlap=true: [[s1, s2, s3],
            [s3, s4, s5], [s5, s6, s7]]
        :return: engine: The LLM engine used.
        sentiment_breakdown: A list of dictionaries representing the score of each segment of
            text. Each dictionary contains the following fields: text: The
            text of the segment. start: The starting character index of the
            segment in the original text. end: The ending character index of
            the segment in the original text. sentiment: A dictionary
            containing the scores for negative, neutral and positive.
        sentiment_overall: Contains the overall negative, neutral and positive score for
            the provided text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/sentiment_analysis.py>`_
        '''
        return super().call(user=user, text=text, engine=engine, sentence_split=sentence_split, sentence_overlap=sentence_overlap)


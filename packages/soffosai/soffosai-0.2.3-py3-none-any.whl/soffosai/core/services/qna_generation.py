'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Qn A Generation Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class QnAGenerationService(SoffosAIService):
    '''
    The Q&A Generation module splits large documents in chunks from which it
    generates multiple question-answer pairs. The chunk length is configurable.
    Usually more questions can be generated when segmenting the text to smaller
    chunks, while longer chunks help retain more context, in cases where a topic is
    discussed over multiple sentences in the context. To address cases where the
    topic is split mid-way, the module supports overlapping the chunks by a
    configurable amount of sentences. This gives a lot of flexibility to cater to
    your specific use case.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.QN_A_GENERATION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None, sentence_split:int=3, sentence_overlap:bool=None) -> dict:
        '''
        Call the Qn A Generation Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: The input text from which the question-answer pairs will be
            generated.
        :param engine: The LLM engine to be used.
        :param sentence_split: The number of sentences of each chunk when splitting the input
            text.
        :param sentence_overlap: Whether to overlap adjacent chunks by 1 sentence. For example,
            with sentence_split 3 and sentence_overlap=true : [[s1, s2, s3],
            [s3, s4, s5], [s5, s6, s7]]
        :return: engine: The LLM engine used.
        qna_list: A list of dictionaries representing question-answer pairs. Each
            dictionary contains the fields question, answer and chunk_index
            which is the index of the chunk the question-answer pair was
            generated from. chunk_index maps to the chunk with the same
            value in the key index.
        chunks: A list of dictionaries representing the chunks as they were
            split from the original according to the splitting parameters
            given in the request. Each dictionary contains the fields text,
            index as well as the span_start and span_end fields which are
            the starting and ending position of the chunk in the originally
            provided text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/qn_a_generation.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine, sentence_split=sentence_split, sentence_overlap=sentence_overlap)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None, sentence_split:Union[int, InputConfig]=3, sentence_overlap:Union[bool, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine, sentence_split=sentence_split, sentence_overlap=sentence_overlap)

    @classmethod
    def call(self, user:str, text:str, engine:str=None, sentence_split:int=3, sentence_overlap:bool=None) -> dict:
        '''
        Call the Qn A Generation Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: The input text from which the question-answer pairs will be
            generated.
        :param engine: The LLM engine to be used.
        :param sentence_split: The number of sentences of each chunk when splitting the input
            text.
        :param sentence_overlap: Whether to overlap adjacent chunks by 1 sentence. For example,
            with sentence_split 3 and sentence_overlap=true : [[s1, s2, s3],
            [s3, s4, s5], [s5, s6, s7]]
        :return: engine: The LLM engine used.
        qna_list: A list of dictionaries representing question-answer pairs. Each
            dictionary contains the fields question, answer and chunk_index
            which is the index of the chunk the question-answer pair was
            generated from. chunk_index maps to the chunk with the same
            value in the key index.
        chunks: A list of dictionaries representing the chunks as they were
            split from the original according to the splitting parameters
            given in the request. Each dictionary contains the fields text,
            index as well as the span_start and span_end fields which are
            the starting and ending position of the chunk in the originally
            provided text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/qn_a_generation.py>`_
        '''
        return super().call(user=user, text=text, engine=engine, sentence_split=sentence_split, sentence_overlap=sentence_overlap)


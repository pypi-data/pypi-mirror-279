'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Answer Scoring Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class AnswerScoringService(SoffosAIService):
    '''
    This module will mark the user's answer based on the provided context, the
    question and, optionally, the expected correct answer. Typical string
    similarity methods often fail to accurately capture the similarity in meaning
    and semantics, especially in cases where a single word can alter the entire
    meaning of a sentence. This module not only addresses this issue, but the fact
    that the underlying AI understands the context and question also enables it to
    evaluate an answer even if the expected correct answer is not provided.
    However, when provided, the evaluation will give it more weight than the
    information in the context. The score is a value between 0 and 1, with 0 being
    completely wrong and 1 being perfectly accurate. Additionally, the reasoning
    behind the score is provided. The Answer Scoring module is a perfect fit to
    supplement the Q&A generation module by marking users' answers to AI-generated
    question-answer pairs. Together they can power a wide range of educational and
    retention-assessment applications.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.ANSWER_SCORING
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, context:str, question:str, user_answer:str, engine:str=None, answer:str=None) -> dict:
        '''
        Call the Answer Scoring Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param context: This should be the passage with the information that is related
            to the question and answer.
        :param question: The question to answer.
        :param user_answer: The user's answer which will be marked.
        :param engine: The LLM engine to be used.
        :param answer: Optionally provide the expected answer.
        :return: engine: The LLM engine used.
        score: A value between 0 and 1 indicating the correctness of the answer.
        reasoning: A concise explanation of how the AI arrived to the predicted
            score.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/answer_scoring.py>`_
        '''
        return super().__call__(user=user, context=context, question=question, user_answer=user_answer, engine=engine, answer=answer)

    def set_input_configs(self, name:str, context:Union[str, InputConfig], question:Union[str, InputConfig], user_answer:Union[str, InputConfig], engine:Union[str, InputConfig]=None, answer:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, context=context, question=question, user_answer=user_answer, engine=engine, answer=answer)

    @classmethod
    def call(self, user:str, context:str, question:str, user_answer:str, engine:str=None, answer:str=None) -> dict:
        '''
        Call the Answer Scoring Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param context: This should be the passage with the information that is related
            to the question and answer.
        :param question: The question to answer.
        :param user_answer: The user's answer which will be marked.
        :param engine: The LLM engine to be used.
        :param answer: Optionally provide the expected answer.
        :return: engine: The LLM engine used.
        score: A value between 0 and 1 indicating the correctness of the answer.
        reasoning: A concise explanation of how the AI arrived to the predicted
            score.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/answer_scoring.py>`_
        '''
        return super().call(user=user, context=context, question=question, user_answer=user_answer, engine=engine, answer=answer)

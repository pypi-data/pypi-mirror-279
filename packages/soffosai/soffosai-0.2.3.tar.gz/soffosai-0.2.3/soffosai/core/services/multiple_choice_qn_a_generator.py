'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-20
Purpose: Easily use Multiple Choice Qn A Generator Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class MultipleChoiceQnAGeneratorService(SoffosAIService):
    '''
    Accepts a context and generates Multiple-Choice Question and Answer sets
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.MULTIPLE_CHOICE_QN_A_GENERATOR
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, context:str, num_questions:int, num_choices:int, engine:str=None) -> dict:
        '''
        Call the Multiple Choice Qn A Generator Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param context: the prompt to be sent to the LLM
        :param num_questions: the location of the image to be processed
        :param num_choices: the location of the image to be processed
        :param engine: The LLM engine to be used.
        :return: qna_sets: The question and answer sets
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/multiple_choice_qn_a_generator.py>`_
        '''
        return super().__call__(user=user, context=context, num_questions=num_questions, num_choices=num_choices, engine=engine)

    def set_input_configs(self, name:str, context:Union[str, InputConfig], num_questions:Union[int, InputConfig], num_choices:Union[int, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, context=context, num_questions=num_questions, num_choices=num_choices, engine=engine)

    @classmethod
    def call(self, user:str, context:str, num_questions:int, num_choices:int, engine:str=None) -> dict:
        '''
        Call the Multiple Choice Qn A Generator Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param context: the prompt to be sent to the LLM
        :param num_questions: the location of the image to be processed
        :param num_choices: the location of the image to be processed
        :param engine: The LLM engine to be used.
        :return: qna_sets: The question and answer sets
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/multiple_choice_qn_a_generator.py>`_
        '''
        return super().call(user=user, context=context, num_questions=num_questions, num_choices=num_choices, engine=engine)


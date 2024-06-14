'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-27
Purpose: Easily use Assessment Generator Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class AssessmentGeneratorService(SoffosAIService):
    '''
    Generates Assesments from a given context
    ----------------------------------------------------- Accepts a context and
    generates Assessments of types/modes: * Multiple Choice, * True or False, *
    Fill in the Blanks * Short Answer
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.ASSESSMENT_GENERATOR
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, context:str, engine:str=None, mode:str="short answer", num_questions:int=10, num_choices:int=3) -> dict:
        '''
        Call the Assessment Generator Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param context: the prompt to be sent to the LLM
        :param engine: The LLM engine to be used.
        :param mode: The type/mode of assessment.
        :param num_questions: the location of the image to be processed
        :param num_choices: the location of the image to be processed
        :return: qna_sets: The question and answer sets
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/assessment_generator.py>`_
        '''
        return super().__call__(user=user, context=context, engine=engine, mode=mode, num_questions=num_questions, num_choices=num_choices)

    def set_input_configs(self, name:str, context:Union[str, InputConfig], engine:Union[str, InputConfig]=None, mode:Union[str, InputConfig]="short answer", num_questions:Union[int, InputConfig]=10, num_choices:Union[int, InputConfig]=3):
        super().set_input_configs(name=name, context=context, engine=engine, mode=mode, num_questions=num_questions, num_choices=num_choices)

    @classmethod
    def call(self, user:str, context:str, engine:str=None, mode:str="short answer", num_questions:int=10, num_choices:int=3) -> dict:
        '''
        Call the Assessment Generator Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param context: the prompt to be sent to the LLM
        :param engine: The LLM engine to be used.
        :param mode: The type/mode of assessment.
        :param num_questions: the location of the image to be processed
        :param num_choices: the location of the image to be processed
        :return: qna_sets: The question and answer sets
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/assessment_generator.py>`_
        '''
        return super().call(user=user, context=context, engine=engine, mode=mode, num_questions=num_questions, num_choices=num_choices)


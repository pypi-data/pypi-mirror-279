'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Microlesson Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class MicrolessonService(SoffosAIService):
    '''
    Accepts a list of texts, each one labelled with its source and creates a
    concise microlesson including a short summary, key points, learning objectives
    and tasks that aim to help the learner achieve the learning objectives.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.MICROLESSON
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, content:list, engine:str=None) -> dict:
        '''
        Call the Microlesson Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param content: A list of dictionaries. Each dictionary should contain the
            'source' and 'text' fields, where 'source' is the name of the
            document/article/website/etc. and 'text' is the actual content.
            Providing the source names enables the microlesson to include
            the source for the key points extracted from the content.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        microlesson: A concise, structured microlesson containing a summary, key
            points, learning objectives and tasks.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/microlesson.py>`_
        '''
        return super().__call__(user=user, content=content, engine=engine)

    def set_input_configs(self, name:str, content:Union[list, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, content=content, engine=engine)

    @classmethod
    def call(self, user:str, content:list, engine:str=None) -> dict:
        '''
        Call the Microlesson Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param content: A list of dictionaries. Each dictionary should contain the
            'source' and 'text' fields, where 'source' is the name of the
            document/article/website/etc. and 'text' is the actual content.
            Providing the source names enables the microlesson to include
            the source for the key points extracted from the content.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        microlesson: A concise, structured microlesson containing a summary, key
            points, learning objectives and tasks.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/microlesson.py>`_
        '''
        return super().call(user=user, content=content, engine=engine)


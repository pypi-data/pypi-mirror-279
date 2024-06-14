'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Tag Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TagService(SoffosAIService):
    '''
    This module can generate tags for a piece of text that can aid with content
    search in certain use-cases. It allows to specify a number of tags to be
    generated for each of the categories "topic", "domain", "audience", "entity".
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TAG
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, engine:str=None, types:list=None, n:int=None) -> dict:
        '''
        Call the Tag Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to extract keywords from.
        :param engine: The LLM engine to be used.
        :param types: List of types of keywords to extract. Supported types: topic:
            Tags relating to the subject matter of the text. domain: Tags
            relating to the domain of the text. For example, 'AI', or
            'Science fiction'. audience: Tags relating to the type of
            audience the text is intended for. entity: Entities such as
            people, places, products, etc. mentioned in the text.
        :param n: The number of tags to be generated for each of the specified tag
            types.
        :return: engine: The LLM engine used.
        tags: A dictionary containing the tags grouped by the type of tag. A
            confidence score is provided also for each tag.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/tag.py>`_
        '''
        return super().__call__(user=user, text=text, engine=engine, types=types, n=n)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], engine:Union[str, InputConfig]=None, types:Union[list, InputConfig]=None, n:Union[int, InputConfig]=None):
        super().set_input_configs(name=name, text=text, engine=engine, types=types, n=n)

    @classmethod
    def call(self, user:str, text:str, engine:str=None, types:list=None, n:int=None) -> dict:
        '''
        Call the Tag Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to extract keywords from.
        :param engine: The LLM engine to be used.
        :param types: List of types of keywords to extract. Supported types: topic:
            Tags relating to the subject matter of the text. domain: Tags
            relating to the domain of the text. For example, 'AI', or
            'Science fiction'. audience: Tags relating to the type of
            audience the text is intended for. entity: Entities such as
            people, places, products, etc. mentioned in the text.
        :param n: The number of tags to be generated for each of the specified tag
            types.
        :return: engine: The LLM engine used.
        tags: A dictionary containing the tags grouped by the type of tag. A
            confidence score is provided also for each tag.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/tag.py>`_
        '''
        return super().call(user=user, text=text, engine=engine, types=types, n=n)


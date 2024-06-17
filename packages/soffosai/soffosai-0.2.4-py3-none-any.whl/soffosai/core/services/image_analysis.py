'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-20
Purpose: Easily use Image Analysis Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ImageAnalysisService(SoffosAIService):
    '''
    The base service for all Image Analyzation Services
    ----------------------------------------------------------- 
    Describes an image
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.IMAGE_ANALYSIS
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, prompt:str, image_url:str, engine:str=None) -> dict:
        '''
        Call the Image Analysis Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param prompt: the prompt to be sent to the LLM
        :param image_url: the location of the image to be processed
        :param engine: The LLM engine to be used.
        :return: analysis: the analysis of the image
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/image_analysis.py>`_
        '''
        return super().__call__(user=user, prompt=prompt, image_url=image_url, engine=engine)

    def set_input_configs(self, name:str, prompt:Union[str, InputConfig], image_url:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, prompt=prompt, image_url=image_url, engine=engine)

    @classmethod
    def call(self, user:str, prompt:str, image_url:str, engine:str=None) -> dict:
        '''
        Call the Image Analysis Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param prompt: the prompt to be sent to the LLM
        :param image_url: the location of the image to be processed
        :param engine: The LLM engine to be used.
        :return: analysis: the analysis of the image
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/image_analysis.py>`_
        '''
        return super().call(user=user, prompt=prompt, image_url=image_url, engine=engine)


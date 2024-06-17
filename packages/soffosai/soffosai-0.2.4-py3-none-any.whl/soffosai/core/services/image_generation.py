'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-21
Purpose: Easily use Image Generation Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class ImageGenerationService(SoffosAIService):
    '''
    The base service for all Image Generation Services
    ----------------------------------------------------------- Create an image
    from a prompt. Can also specify size, engine to be used, quality and quantity
    of images to be generated.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.IMAGE_GENERATION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, prompt:str, engine:str=None, size:str="1024x1024", quality:str="standard", quantity:int=1) -> dict:
        '''
        Call the Image Generation Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param prompt: the prompt to be sent to the LLM.
        :param engine: The LLM engine to be used.
        :param size: the required size of the image.
        :param quality: the quality of the image
        :param quantity: how many images should be created
        :return: image_urls: list of image URLs
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/image_generation.py>`_
        '''
        return super().__call__(user=user, prompt=prompt, engine=engine, size=size, quality=quality, quantity=quantity)

    def set_input_configs(self, name:str, prompt:Union[str, InputConfig], engine:Union[str, InputConfig]=None, size:Union[str, InputConfig]="1024x1024", quality:Union[str, InputConfig]="standard", quantity:Union[int, InputConfig]=1):
        super().set_input_configs(name=name, prompt=prompt, engine=engine, size=size, quality=quality, quantity=quantity)

    @classmethod
    def call(self, user:str, prompt:str, engine:str=None, size:str="1024x1024", quality:str="standard", quantity:int=1) -> dict:
        '''
        Call the Image Generation Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param prompt: the prompt to be sent to the LLM.
        :param engine: The LLM engine to be used.
        :param size: the required size of the image.
        :param quality: the quality of the image
        :param quantity: how many images should be created
        :return: image_urls: list of image URLs
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/image_generation.py>`_
        '''
        return super().call(user=user, prompt=prompt, engine=engine, size=size, quality=quality, quantity=quantity)


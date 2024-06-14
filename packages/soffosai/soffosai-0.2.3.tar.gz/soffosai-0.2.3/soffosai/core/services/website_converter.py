'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Website Converter Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class WebsiteConverterService(SoffosAIService):
    '''
    The Website Converter module offers basic functionality for extracting
    meaningful text from websites. This can be a useful tool for processing website
    content with other modules. Note: Character volume is not charged for this
    module.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.WEBSITE_CONVERTER
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, url:str, engine:str=None) -> dict:
        '''
        Call the Website Converter Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param url: The url to extract text from.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        text: Raw text extracted from the website.
        links: A dictionary containing a list of `internal` and a list of
            `external` links found on the website. `internal`: Links found
            on the page that are under the same domain as the provided url.
            `external`: Links found on the page that belong to different
            domains.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/website_converter.py>`_
        '''
        return super().__call__(user=user, url=url, engine=engine)

    def set_input_configs(self, name:str, url:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, url=url, engine=engine)

    @classmethod
    def call(self, user:str, url:str, engine:str=None) -> dict:
        '''
        Call the Website Converter Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param url: The url to extract text from.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        text: Raw text extracted from the website.
        links: A dictionary containing a list of `internal` and a list of
            `external` links found on the website. `internal`: Links found
            on the page that are under the same domain as the provided url.
            `external`: Links found on the page that belong to different
            domains.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/website_converter.py>`_
        '''
        return super().call(user=user, url=url, engine=engine)


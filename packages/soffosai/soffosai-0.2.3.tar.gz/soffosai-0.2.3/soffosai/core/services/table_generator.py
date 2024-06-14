'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Table Generator Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TableGeneratorService(SoffosAIService):
    '''
    The table generator module enables applications to extract numerical and
    statistical data from raw text in a tabular format. For use-cases where data
    has to be manually reviewed and cross-referenced, this module can bring
    enormous value.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TABLE_GENERATOR
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, table_format:str, engine:str=None, topic:str=None) -> dict:
        '''
        Call the Table Generator Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to extract tables from.
        :param table_format: A string indicating the table output format. Formats supported:
            markdown, CSV
        :param engine: The LLM engine to be used.
        :param topic: A short text that describes what kind of information should be
            extracted.
        :return: engine: The LLM engine used.
        tables: A list of dictionaries representing tables. Each dictionary
            contains the following fields: title: A descriptive title for
            the table table: The table in a raw markdown or CSV formatted
            string. note: Useful notes for table interpretation.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_generator.py>`_
        '''
        return super().__call__(user=user, text=text, table_format=table_format, engine=engine, topic=topic)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], table_format:Union[str, InputConfig], engine:Union[str, InputConfig]=None, topic:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, text=text, table_format=table_format, engine=engine, topic=topic)

    @classmethod
    def call(self, user:str, text:str, table_format:str, engine:str=None, topic:str=None) -> dict:
        '''
        Call the Table Generator Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to extract tables from.
        :param table_format: A string indicating the table output format. Formats supported:
            markdown, CSV
        :param engine: The LLM engine to be used.
        :param topic: A short text that describes what kind of information should be
            extracted.
        :return: engine: The LLM engine used.
        tables: A list of dictionaries representing tables. Each dictionary
            contains the following fields: title: A descriptive title for
            the table table: The table in a raw markdown or CSV formatted
            string. note: Useful notes for table interpretation.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_generator.py>`_
        '''
        return super().call(user=user, text=text, table_format=table_format, engine=engine, topic=topic)


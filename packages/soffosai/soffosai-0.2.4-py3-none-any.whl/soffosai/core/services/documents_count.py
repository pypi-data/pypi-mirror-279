'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Documents Count Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class DocumentsCountService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.DOCUMENTS_COUNT
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, engine:str=None, filters:dict=None, date_from:str=None, date_until:str=None) -> dict:
        '''
        Call the Documents Count Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param filters: The filters field can be used to narrow down the search to only
            the documents meeting certain metadata-based criteria, or even
            returning all the filtered documents when query is left null.
        :param date_from: Filters passages to those ingested at or after the specified
            ISO-8601 formatted date.
        :param date_until: Filters passages to those ingested before the specified ISO-8601
            formatted date.
        :return: engine: The LLM engine used.
        documents: A list of objects representing documents. Information provided
            is the document name, ID and metadata. The content is not
            included.
        count: The document count.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_count.py>`_
        '''
        return super().__call__(user=user, engine=engine, filters=filters, date_from=date_from, date_until=date_until)

    def set_input_configs(self, name:str, engine:Union[str, InputConfig]=None, filters:Union[dict, InputConfig]=None, date_from:Union[str, InputConfig]=None, date_until:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, engine=engine, filters=filters, date_from=date_from, date_until=date_until)

    @classmethod
    def call(self, user:str, engine:str=None, filters:dict=None, date_from:str=None, date_until:str=None) -> dict:
        '''
        Call the Documents Count Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param filters: The filters field can be used to narrow down the search to only
            the documents meeting certain metadata-based criteria, or even
            returning all the filtered documents when query is left null.
        :param date_from: Filters passages to those ingested at or after the specified
            ISO-8601 formatted date.
        :param date_until: Filters passages to those ingested before the specified ISO-8601
            formatted date.
        :return: engine: The LLM engine used.
        documents: A list of objects representing documents. Information provided
            is the document name, ID and metadata. The content is not
            included.
        count: The document count.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_count.py>`_
        '''
        return super().call(user=user, engine=engine, filters=filters, date_from=date_from, date_until=date_until)


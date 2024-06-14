'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Documents Search Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class DocumentsSearchService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.DOCUMENTS_SEARCH
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, engine:str=None, query:str=None, document_ids:list=None, top_n_keyword:int=5, top_n_natural_language:int=5, filters:dict=None, date_from:str=None, date_until:str=None) -> dict:
        '''
        Call the Documents Search Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param query: The text to be used to match passages from ingested documents.
        :param document_ids: Passing document IDs will confine the search to those documents.
        :param top_n_keyword: The number of document passages to be retrieved using keyword
            search.
        :param top_n_natural_language: The number of document passages to be retrieved using Machine
            Learning-based semantic search.
        :param filters: The filters field can be used to narrow down the search to only
            the documents meeting certain metadata-based criteria, or even
            returning all the filtered documents when query is left null.
        :param date_from: Filters passages to those ingested at or after the specified
            ISO-8601 formatted date.
        :param date_until: Filters passages to those ingested before the specified ISO-8601
            formatted date.
        :return: engine: The LLM engine used.
        passages: List of passages. Each passage contains the following data:
            content: The raw text of the passage. document_id: Origin
            document's ID. created_at: Ingestion datetime. name: Origin
            document's name. scores: Dictionary containing the matching
            score of this passage to the query for each method that matched
            it. meta: Dictionary with the metadata that were provided when
            the passage's origin document was ingested.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_search.py>`_
        '''
        return super().__call__(user=user, engine=engine, query=query, document_ids=document_ids, top_n_keyword=top_n_keyword, top_n_natural_language=top_n_natural_language, filters=filters, date_from=date_from, date_until=date_until)

    def set_input_configs(self, name:str, engine:Union[str, InputConfig]=None, query:Union[str, InputConfig]=None, document_ids:Union[list, InputConfig]=None, top_n_keyword:Union[int, InputConfig]=5, top_n_natural_language:Union[int, InputConfig]=5, filters:Union[dict, InputConfig]=None, date_from:Union[str, InputConfig]=None, date_until:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, engine=engine, query=query, document_ids=document_ids, top_n_keyword=top_n_keyword, top_n_natural_language=top_n_natural_language, filters=filters, date_from=date_from, date_until=date_until)

    @classmethod
    def call(self, user:str, engine:str=None, query:str=None, document_ids:list=None, top_n_keyword:int=5, top_n_natural_language:int=5, filters:dict=None, date_from:str=None, date_until:str=None) -> dict:
        '''
        Call the Documents Search Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param query: The text to be used to match passages from ingested documents.
        :param document_ids: Passing document IDs will confine the search to those documents.
        :param top_n_keyword: The number of document passages to be retrieved using keyword
            search.
        :param top_n_natural_language: The number of document passages to be retrieved using Machine
            Learning-based semantic search.
        :param filters: The filters field can be used to narrow down the search to only
            the documents meeting certain metadata-based criteria, or even
            returning all the filtered documents when query is left null.
        :param date_from: Filters passages to those ingested at or after the specified
            ISO-8601 formatted date.
        :param date_until: Filters passages to those ingested before the specified ISO-8601
            formatted date.
        :return: engine: The LLM engine used.
        passages: List of passages. Each passage contains the following data:
            content: The raw text of the passage. document_id: Origin
            document's ID. created_at: Ingestion datetime. name: Origin
            document's name. scores: Dictionary containing the matching
            score of this passage to the query for each method that matched
            it. meta: Dictionary with the metadata that were provided when
            the passage's origin document was ingested.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_search.py>`_
        '''
        return super().call(user=user, engine=engine, query=query, document_ids=document_ids, top_n_keyword=top_n_keyword, top_n_natural_language=top_n_natural_language, filters=filters, date_from=date_from, date_until=date_until)


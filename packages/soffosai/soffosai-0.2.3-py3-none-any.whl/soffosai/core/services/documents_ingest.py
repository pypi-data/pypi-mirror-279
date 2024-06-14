'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Documents Ingest Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class DocumentsIngestService(SoffosAIService):
    '''
    The Documents module enables ingestion of contnent into Soffos. The content is
    pre-processed and stored alongside its representations and metadata required
    for searching using natural language. Queries can be as simple as questions
    that someone would ask a human. Additionally, content can be filtered based on
    the metadata provided by the user when ingesting a document. The combination of
    basic filtering similar to how most databases work in combination with natural
    language search, both keyword-based and semantic using machine learning, makes
    this module a very useful tool for any type of use-case that requires lighning
    fast information extraction from large knowledge bases.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.DOCUMENTS_INGEST
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, engine:str=None, meta:dict=None, document_name:str=None, text:str=None, tagged_elements:list=None) -> dict:
        '''
        Call the Documents Ingest Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param meta: A dictionary containing metadata fields for tagging the
            document. The keys should be string and the values can be any
            type, such as string, integer, boolean etc. This allows document
            filtering based on the meta fields. Due to name being a
            mandatory field provided independently, if a name field is
            included in meta it will be ignored. TIP: Only tag your
            documents with metadata that you absolutely need. Avoid long
            values as that adds up to the storage consumption.
        :param document_name: The name of the document.
        :param text: The text content of the document.
        :param tagged_elements: A list of dictionaries representing tagged spans of text
            extracted from a document file.
        :return: engine: The LLM engine used.
        success: Flag that identifies if the API call succeeded or not.
        document_id: The reference ID of the uploaded document.
        filtered: List of passages not included in ingestion due to some profanity
            or errors.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_ingest.py>`_
        '''
        return super().__call__(user=user, engine=engine, meta=meta, document_name=document_name, text=text, tagged_elements=tagged_elements)

    def set_input_configs(self, name:str, engine:Union[str, InputConfig]=None, meta:Union[dict, InputConfig]=None, document_name:Union[str, InputConfig]=None, text:Union[str, InputConfig]=None, tagged_elements:Union[list, InputConfig]=None):
        super().set_input_configs(name=name, engine=engine, meta=meta, document_name=document_name, text=text, tagged_elements=tagged_elements)

    @classmethod
    def call(self, user:str, engine:str=None, meta:dict=None, document_name:str=None, text:str=None, tagged_elements:list=None) -> dict:
        '''
        Call the Documents Ingest Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param engine: The LLM engine to be used.
        :param meta: A dictionary containing metadata fields for tagging the
            document. The keys should be string and the values can be any
            type, such as string, integer, boolean etc. This allows document
            filtering based on the meta fields. Due to name being a
            mandatory field provided independently, if a name field is
            included in meta it will be ignored. TIP: Only tag your
            documents with metadata that you absolutely need. Avoid long
            values as that adds up to the storage consumption.
        :param document_name: The name of the document.
        :param text: The text content of the document.
        :param tagged_elements: A list of dictionaries representing tagged spans of text
            extracted from a document file.
        :return: engine: The LLM engine used.
        success: Flag that identifies if the API call succeeded or not.
        document_id: The reference ID of the uploaded document.
        filtered: List of passages not included in ingestion due to some profanity
            or errors.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_ingest.py>`_
        '''
        return super().call(user=user, engine=engine, meta=meta, document_name=document_name, text=text, tagged_elements=tagged_elements)


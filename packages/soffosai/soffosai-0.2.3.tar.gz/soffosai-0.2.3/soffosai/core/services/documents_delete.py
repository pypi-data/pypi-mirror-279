'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Documents Delete Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class DocumentsDeleteService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.DOCUMENTS_DELETE
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, document_ids:list, engine:str=None) -> dict:
        '''
        Call the Documents Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param document_ids: A list of the document_ids of the documents to be deleted.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        success: Flag that identifies if the API call succeeded or not.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_delete.py>`_
        '''
        return super().__call__(user=user, document_ids=document_ids, engine=engine)

    def set_input_configs(self, name:str, document_ids:Union[list, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, document_ids=document_ids, engine=engine)

    @classmethod
    def call(self, user:str, document_ids:list, engine:str=None) -> dict:
        '''
        Call the Documents Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param document_ids: A list of the document_ids of the documents to be deleted.
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        success: Flag that identifies if the API call succeeded or not.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/documents_delete.py>`_
        '''
        return super().call(user=user, document_ids=document_ids, engine=engine)


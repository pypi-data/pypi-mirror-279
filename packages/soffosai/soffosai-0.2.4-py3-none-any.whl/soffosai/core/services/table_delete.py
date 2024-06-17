'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Table Delete Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TableDeleteService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TABLE_DELETE
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, table_ids:list, engine:str=None) -> dict:
        '''
        Call the Table Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param table_ids: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        success: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_delete.py>`_
        '''
        return super().__call__(user=user, table_ids=table_ids, engine=engine)

    def set_input_configs(self, name:str, table_ids:Union[list, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, table_ids=table_ids, engine=engine)

    @classmethod
    def call(self, user:str, table_ids:list, engine:str=None) -> dict:
        '''
        Call the Table Delete Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param table_ids: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        success: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_delete.py>`_
        '''
        return super().call(user=user, table_ids=table_ids, engine=engine)


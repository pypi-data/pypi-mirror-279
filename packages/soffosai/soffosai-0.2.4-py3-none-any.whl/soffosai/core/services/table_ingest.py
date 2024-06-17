'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Table Ingest Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class TableIngestService(SoffosAIService):
    '''
    General HTTP service client.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.TABLE_INGEST
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, table:list, table_name:str, description:str, engine:str=None) -> dict:
        '''
        Call the Table Ingest Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param table: None
        :param table_name: None
        :param description: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        table_id: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_ingest.py>`_
        '''
        return super().__call__(user=user, table=table, table_name=table_name, description=description, engine=engine)

    def set_input_configs(self, name:str, table:Union[list, InputConfig], table_name:Union[str, InputConfig], description:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, table=table, table_name=table_name, description=description, engine=engine)

    @classmethod
    def call(self, user:str, table:list, table_name:str, description:str, engine:str=None) -> dict:
        '''
        Call the Table Ingest Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param table: None
        :param table_name: None
        :param description: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        table_id: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/table_ingest.py>`_
        '''
        return super().call(user=user, table=table, table_name=table_name, description=description, engine=engine)


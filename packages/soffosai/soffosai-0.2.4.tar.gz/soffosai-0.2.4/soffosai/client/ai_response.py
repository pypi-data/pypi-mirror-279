'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-04-19
Purpose: Hold the output response of Soffos API in an object
-----------------------------------------------------
'''
import json
from soffosai.common.service_io_map import SERVICE_IO_MAP

class SoffosAiResponse:
    '''
    Holds the Soffos AI response
    '''
    def __init__(self, service, raw,**kwargs) -> None:
        self._raw:dict = raw
        self._context = self._raw.get("context")
        self._cost = self._raw.get("cost")
        self._charged_character_count = self._raw.get("charged_character_count")
        self._response = self._raw.get(SERVICE_IO_MAP[service].primary_output_key)
        self._tagged_elements = self._raw.get("tagged_elements")
        self._document_ids = self._raw.get("document_ids")
        other_document_ids = self.look_for_document_ids(self._raw)
        if len(other_document_ids) > 0:
            if self._document_ids:
                self._document_ids.append(other_document_ids)
            else:
                self._document_ids = [other_document_ids]
            
            self._raw['document_ids'] = self._document_ids
        
    @property
    def context(self):
        '''
        The context where the reply is based on
        '''
        return self._context

    @property
    def raw_response(self) -> dict:
        '''
        The raw json response from the ai but converted into a dictionary
        '''
        return self._raw

    @property
    def cost(self) -> dict:
        '''
        a dictionary describing the cost of the api call
        '''
        return self._cost

    @property
    def charged_character_count(self):
        '''
        The number of characters charged. It is based on input or output whichever is higher
        '''
        return self._charged_character_count

    @property
    def response(self) -> str or dict:
        '''
        The common response
        '''
        return self._response

    @property
    def tagged_elements(self):
        '''
        The tagged elements that can be used to optimize document ingestion.
        This is an output of the file converter and is useful for the document ingestion service
        '''
        return self._tagged_elements

    @property
    def document_ids(self):
        return self._document_ids
    
    def look_for_document_ids(self, raw:dict):
        document_ids = []
        if "document_id" in raw:
            document_ids.append(raw['document_id'])
        
        if "document_ids" in raw:
            document_ids.extend(raw['document_ids'])

        for key in raw.keys():
            if isinstance(raw[key], dict):
                if "document_id" in raw[key]:
                    document_ids.append(raw[key]['document_id'])
                if "document_ids" in raw[key]:
                    document_ids.extend(raw[key]['document_ids'])
        
        return document_ids


    def __str__(self) -> str:
        return self._response if isinstance(self._response, str) else json.dumps(self._response, indent=4)

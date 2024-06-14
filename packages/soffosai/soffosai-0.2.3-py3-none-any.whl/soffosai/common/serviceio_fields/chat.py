'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Chat Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ChatIO(ServiceIO):
    service = ServiceString.CHAT
    required_input_fields = ["mode"]
    optional_input_fields = ["session_id","engine","user_id","message","messages","knowledge","document_ids"]
    input_structure = {
        "session_id": str, 
        "engine": str, 
        "user_id": str, 
        "message": str, 
        "messages": list, 
        "mode": str, 
        "knowledge": str, 
        "document_ids": list
    }

    output_structure = {
        "engine": str,
        "messages": list,
        "response": str,
        "session_name": str
    }


    @classmethod
    def special_validation(self, payload):

        # Error if neither message or messages were provided
        if not payload.get('message') and not payload.get('messages'):
            return False, 'One of fields "message" and "messages" must be provided.'
        # Error if both message and messages were provided
        if payload.get('message') and payload.get('messages') is not None:
            return False, 'Only one of fields "message" and "messages" can be provided.'
        # Error if mode is closed or hybrid but no knowledge was provided
        if payload.get('mode') in ['closed', 'hybrid']:
            if not payload.get('knowledge') and not payload.get('document_ids'):
                return False, 'Value of knowledge or document_ids please select a document must be provided when mode is closed or hybrid.'
            if payload.get('knowledge') and payload.get('document_ids'):
                return False, 'Must not provide both knowledge and document_ids arguments.'
            if payload.get('document_ids'):
                if len(payload['document_ids']) < 1:
                    return False, 'The argument <document_ids> cannot be an empty list.'
        
        if payload.get('message'):
            message = payload.get('message')
        else:
            message = payload['messages'][-1]['text']
            
        if len(message) > 20000 and payload.get('mode') in ['closed', 'hybrid']:
            return False, 'Input cannot exceed 20000 characters in closed/hybrid mode.'
        if len(message) > 75000 and payload.get('mode') == 'open':
            return False, 'Input cannot exceed 75000 characters in open mode.'
            
        return super().special_validation(payload)
'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Chat Bot Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ChatBotIO(ServiceIO):
    service = ServiceString.CHAT_BOT
    required_input_fields = ["message","chatbot_id","user_id","mode"]
    optional_input_fields = ["session_id","engine","previous_messages","bot_document_ids","context_document_ids"]
    input_structure = {
        "session_id": str, 
        "engine": str, 
        "message": str, 
        "chatbot_id": str, 
        "previous_messages": list, 
        "user_id": str, 
        "mode": str, 
        "bot_document_ids": list, 
        "context_document_ids": list
    }

    output_structure = {
        "engine": str,
        "context_document_ids": list,
        "response": str,
        "session_name": str,
        "messages": list,
        "context": str
    }


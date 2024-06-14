'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Chat Bot Create Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ChatBotCreateIO(ServiceIO):
    service = ServiceString.CHAT_BOT_CREATE
    required_input_fields = ["role","chatbot_name"]
    optional_input_fields = ["engine","chatbot_id"]
    input_structure = {
        "engine": str, 
        "role": str, 
        "chatbot_name": str, 
        "chatbot_id": str
    }

    output_structure = {
        "engine": str,
        "chatbot_id": str
    }


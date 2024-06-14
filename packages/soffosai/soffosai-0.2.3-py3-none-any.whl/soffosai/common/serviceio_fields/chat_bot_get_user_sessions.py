'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Chat Bot Get User Sessions Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ChatBotGetUserSessionsIO(ServiceIO):
    service = ServiceString.CHAT_BOT_GET_USER_SESSIONS
    required_input_fields = ["chatbot_id","user_id"]
    optional_input_fields = ["engine","session_ids"]
    input_structure = {
        "engine": str, 
        "chatbot_id": str, 
        "user_id": str, 
        "session_ids": list
    }

    output_structure = {
        "engine": str,
        "sessions": dict
    }


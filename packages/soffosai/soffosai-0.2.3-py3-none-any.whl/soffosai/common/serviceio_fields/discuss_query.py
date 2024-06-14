'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Discuss Query Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussQueryIO(ServiceIO):
    service = ServiceString.DISCUSS_QUERY
    required_input_fields = ["query"]
    optional_input_fields = ["engine", "session_id"]
    input_structure = {
        "engine": str, 
        "query": str,
        "session_id": str,
    }

    output_structure = {
        "engine": str,
        "response": str,
        "context": str,
        "messages": list
    }


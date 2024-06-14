'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Discuss Count Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussCountIO(ServiceIO):
    service = ServiceString.DISCUSS_COUNT
    required_input_fields = ["return_messages"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "return_messages": bool
    }

    output_structure = {
        "engine": str,
        "sessions": list,
        "session_count": int
    }


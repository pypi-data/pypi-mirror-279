'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Discuss Delete Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussDeleteIO(ServiceIO):
    service = ServiceString.DISCUSS_DELETE
    required_input_fields = []
    optional_input_fields = ["engine","session_ids"]
    input_structure = {
        "engine": str, 
        "session_ids": list
    }

    output_structure = {
        "engine": str,
        "success": bool
    }


'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Tag Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TagIO(ServiceIO):
    service = ServiceString.TAG
    required_input_fields = ["text"]
    optional_input_fields = ["engine","types","n"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "types": list, 
        "n": int
    }

    output_structure = {
        "engine": str,
        "tags": dict
    }

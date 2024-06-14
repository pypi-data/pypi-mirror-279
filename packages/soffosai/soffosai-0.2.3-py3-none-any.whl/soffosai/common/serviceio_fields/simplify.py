'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Simplify Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class SimplifyIO(ServiceIO):
    service = ServiceString.SIMPLIFY
    required_input_fields = ["text"]
    optional_input_fields = ["engine","age"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "age": int
    }

    output_structure = {
        "engine": str,
        "simplify": str
    }

'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Table Generator Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TableGeneratorIO(ServiceIO):
    service = ServiceString.TABLE_GENERATOR
    required_input_fields = ["text","table_format"]
    optional_input_fields = ["engine","topic"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "table_format": str, 
        "topic": str
    }

    output_structure = {
        "engine": str,
        "tables": dict
    }


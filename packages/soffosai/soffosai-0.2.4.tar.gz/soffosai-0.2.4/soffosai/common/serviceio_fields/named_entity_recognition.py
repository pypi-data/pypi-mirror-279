'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for N E R Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class NERIO(ServiceIO):
    service = ServiceString.N_E_R
    required_input_fields = ["text"]
    optional_input_fields = ["engine","labels"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "labels": dict
    }

    output_structure = {
        "engine": str,
        "named_entities": list,
        "highlight_html": str
    }

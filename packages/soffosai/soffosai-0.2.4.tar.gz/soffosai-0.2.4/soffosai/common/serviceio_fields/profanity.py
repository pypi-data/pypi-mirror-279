'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Profanity Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ProfanityIO(ServiceIO):
    service = ServiceString.PROFANITY
    required_input_fields = ["text"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "text": str
    }

    output_structure = {
        "engine": str,
        "profanities": list,
        "offensive_probability": float,
        "offensive_prediction": bool
    }


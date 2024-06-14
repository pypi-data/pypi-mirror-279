'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Language Detection Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class LanguageDetectionIO(ServiceIO):
    service = ServiceString.LANGUAGE_DETECTION
    required_input_fields = ["text"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "text": str
    }

    output_structure = {
        "engine": str,
        "language": dict
    }


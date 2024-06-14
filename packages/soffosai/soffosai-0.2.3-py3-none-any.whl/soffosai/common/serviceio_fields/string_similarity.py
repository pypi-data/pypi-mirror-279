'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for String Similarity Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class StringSimilarityIO(ServiceIO):
    service = ServiceString.STRING_SIMILARITY
    required_input_fields = ["a","b"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "a": str, 
        "b": str
    }

    output_structure = {
        "engine": str,
        "score": float,
        "text_spans": dict
    }


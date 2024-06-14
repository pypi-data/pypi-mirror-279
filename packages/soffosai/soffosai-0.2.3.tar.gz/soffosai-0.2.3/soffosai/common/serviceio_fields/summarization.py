'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Summarization Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class SummarizationIO(ServiceIO):
    service = ServiceString.SUMMARIZATION
    required_input_fields = ["text","sent_length"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "sent_length": int
    }

    output_structure = {
        "engine": str,
        "summary": str
    }

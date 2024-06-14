'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Email Analysis Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class EmailAnalysisIO(ServiceIO):
    service = ServiceString.EMAIL_ANALYSIS
    required_input_fields = ["text"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "text": str
    }

    output_structure = {
        "engine": str,
        "analysis": dict
    }


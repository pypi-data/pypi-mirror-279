'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-27
Purpose: Input/Output description for Assessment Generator Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class AssessmentGeneratorIO(ServiceIO):
    service = ServiceString.ASSESSMENT_GENERATOR
    required_input_fields = ["context"]
    optional_input_fields = ["engine","mode","num_questions","num_choices"]
    input_structure = {
        "engine": str, 
        "context": str, 
        "mode": str, 
        "num_questions": int, 
        "num_choices": int
    }

    output_structure = {
        "qna_sets": list
    }

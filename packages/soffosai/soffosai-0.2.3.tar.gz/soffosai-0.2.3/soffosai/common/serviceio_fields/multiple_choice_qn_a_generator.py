'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-20
Purpose: Input/Output description for Multiple Choice Qn A Generator Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class MultipleChoiceQnAGeneratorIO(ServiceIO):
    service = ServiceString.MULTIPLE_CHOICE_QN_A_GENERATOR
    required_input_fields = ["context"]
    optional_input_fields = ["engine","num_questions","num_choices"]
    input_structure = {
        "engine": str, 
        "context": str, 
        "num_questions": int, 
        "num_choices": int
    }

    output_structure = {
        "qna_sets": list
    }


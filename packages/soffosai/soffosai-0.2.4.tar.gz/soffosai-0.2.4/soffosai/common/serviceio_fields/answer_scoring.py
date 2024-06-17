'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Answer Scoring Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class AnswerScoringIO(ServiceIO):
    service = ServiceString.ANSWER_SCORING
    required_input_fields = ["context","question","user_answer"]
    optional_input_fields = ["engine","answer"]
    input_structure = {
        "engine": str, 
        "context": str, 
        "question": str, 
        "answer": str, 
        "user_answer": str
    }

    output_structure = {
        "engine": str,
        "score": float,
        "reasoning": str
    }


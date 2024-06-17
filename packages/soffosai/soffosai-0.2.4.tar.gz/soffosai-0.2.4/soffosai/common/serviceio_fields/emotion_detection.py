'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Emotion Detection Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class EmotionDetectionIO(ServiceIO):
    service = ServiceString.EMOTION_DETECTION
    required_input_fields = ["text","sentence_split","sentence_overlap"]
    optional_input_fields = ["engine","emotion_choices"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "sentence_split": int, 
        "sentence_overlap": bool, 
        "emotion_choices": list
    }

    output_structure = {
        "engine": str,
        "spans": dict
    }


    @classmethod
    def special_validation(self, payload):
        
        
        if payload["sentence_split"] == 1 and payload["sentence_overlap"] == True:
            return False, 'Value "sentence_overlap" must be false when "sentence_split" is set to 1.'
        
        if 'emotion_choices' in payload:
            payload['emotion_choices'] = list(payload['emotion_choices'])
            if not payload['emotion_choices']:
                payload['emotion_choices'] = choices
            
        payload['sentence_overlap'] = 1 if payload['sentence_overlap'] else 0

        return super().special_validation(payload)
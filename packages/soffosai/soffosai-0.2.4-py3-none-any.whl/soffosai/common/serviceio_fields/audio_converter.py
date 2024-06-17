'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Audio Converter Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString
from io import BufferedReader


class AudioConverterIO(ServiceIO):
    service = ServiceString.AUDIO_CONVERTER
    required_input_fields = ["diarize"]
    optional_input_fields = ["file","url","model"]
    input_structure = {
        "file": (BufferedReader, str), 
        "url": str, 
        "model": str, 
        "diarize": bool
    }

    output_structure = {
        "number_of_speakers": int,
        "transcripts": dict,
        "language": str,
        "error": str
    }


    @classmethod
    def special_validation(self, payload):
        
        if payload.get("file") and payload.get('url'):
            return False, "Please provide file or url, not both."
        
        if not payload.get("file") and not payload.get('url'):
            return (False, "Please provide the auido file or url of the audio file.")

        AVAILABLE_MODELS = ("whisper", "nova 2")

        if payload.get("model"):
            if (payload.get("model")).lower() not in AVAILABLE_MODELS:
                return (False, "model field's value can only be 'whisper' or 'nova 2'.")

        return super().special_validation(payload)
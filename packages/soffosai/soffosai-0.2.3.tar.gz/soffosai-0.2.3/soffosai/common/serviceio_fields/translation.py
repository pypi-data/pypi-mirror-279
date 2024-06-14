'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Translation Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TranslationIO(ServiceIO):
    service = ServiceString.TRANSLATION
    required_input_fields = ["text"]
    optional_input_fields = ["engine","auto_detect","source_language_code","target_language_code"]
    input_structure = {
        "engine": str, 
        "text": str, 
        "auto_detect": bool, 
        "source_language_code": str, 
        "target_language_code": str
    }

    output_structure = {
        "engine": str,
        "target_language_code": str,
        "translation": dict
    }


    @classmethod
    def special_validation(self, payload):
        

        if payload.get("auto_detect") and payload.get("source_language_code"):
            return False, "When specifying a \"source_language_code\", set \"auto_detect\" to false. Note that enabling \"auto_detect\" incurs extra costs."
        if not payload.get("auto_detect") and not payload.get("source_language_code"):
            return False, "Please specify a \"source_language_code\". Otherwise, set \"auto_detect\" to True."
        if payload.get("target_language_code") and payload.get("source_language_code"):
            if payload["target_language_code"] == payload["source_language_code"]:
                return False, "Source and target language code can not be the same."

        return super().special_validation(payload)
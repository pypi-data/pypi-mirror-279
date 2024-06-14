'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Documents Count Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DocumentsCountIO(ServiceIO):
    service = ServiceString.DOCUMENTS_COUNT
    required_input_fields = []
    optional_input_fields = ["engine","filters","date_from","date_until"]
    input_structure = {
        "engine": str, 
        "filters": dict, 
        "date_from": str, 
        "date_until": str
    }

    output_structure = {
        "engine": str,
        "documents": dict,
        "count": int
    }


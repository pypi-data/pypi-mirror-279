'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Documents Delete Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DocumentsDeleteIO(ServiceIO):
    service = ServiceString.DOCUMENTS_DELETE
    required_input_fields = ["document_ids"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "document_ids": list
    }

    output_structure = {
        "engine": str,
        "success": bool
    }


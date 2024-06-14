'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Table Ingest Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TableIngestIO(ServiceIO):
    service = ServiceString.TABLE_INGEST
    required_input_fields = ["table","name","description"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "table": list, 
        "name": str, 
        "description": str
    }

    output_structure = {
        "engine": str,
        "table_id": str
    }


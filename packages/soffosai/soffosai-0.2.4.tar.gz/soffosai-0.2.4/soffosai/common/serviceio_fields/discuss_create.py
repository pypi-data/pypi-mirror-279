'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Discuss Create Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussCreateIO(ServiceIO):
    service = ServiceString.DISCUSS_CREATE
    required_input_fields = ["context"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "context": str
    }

    output_structure = {
        "engine": str
    }


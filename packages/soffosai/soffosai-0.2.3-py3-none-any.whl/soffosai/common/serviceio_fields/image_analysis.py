'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-20
Purpose: Input/Output description for Image Analysis Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ImageAnalysisIO(ServiceIO):
    service = ServiceString.IMAGE_ANALYSIS
    required_input_fields = ["prompt","image_url"]
    optional_input_fields = ["engine"]
    input_structure = {
        "engine": str, 
        "prompt": str, 
        "image_url": str
    }

    output_structure = {
        "analysis": str
    }


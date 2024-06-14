'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-20
Purpose: Input/Output description for Image Generation Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ImageGenerationIO(ServiceIO):
    service = ServiceString.IMAGE_GENERATION
    required_input_fields = ["prompt"]
    optional_input_fields = ["engine","size","quality","quantity"]
    input_structure = {
        "engine": str, 
        "prompt": str, 
        "size": str, 
        "quality": str, 
        "quantity": int
    }

    output_structure = {
        "image_urls": list
    }


'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Input/Output description for Documents Ingest Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DocumentsIngestIO(ServiceIO):
    service = ServiceString.DOCUMENTS_INGEST
    required_input_fields = []
    optional_input_fields = ["engine","meta","document_name","text","tagged_elements"]
    input_structure = {
        "engine": str, 
        "meta": dict, 
        "document_name": str, 
        "text": str, 
        "tagged_elements": list
    }

    output_structure = {
        "engine": str,
        "success": bool,
        "document_id": str,
        "filtered": dict
    }


    @classmethod
    def special_validation(self, payload):
        
        if payload.get('text') is not None and payload.get('tagged_elements') is not None:
            return False, 'Only one of "text" and "tagged_elements" can be provided.'
        if not payload.get('text') and not payload.get('tagged_elements'):
            return False, 'No "text" or "tagged_elements" were provided.'
        if payload.get('tagged_elements'):
            for i, elem_dict in enumerate(payload['tagged_elements']):
                # Validate that "text" is present
                if 'text' not in elem_dict:
                    return False, \
                        '"tagged_elements" data is corrupted. '\
                        f'Element at index {i} has no attribute "text".'
                # Validate that "tag" is present
                if 'tag' not in elem_dict:
                    return False, \
                        '"tagged_elements" data is corrupted. '\
                        f'Element at index {i} has no attribute "tag".'
                # Validate that "text" is a string
                if not isinstance(elem_dict.get('text'), str):
                    return False, \
                        '"tagged_elements" data is corrupted. '\
                        f'Field "text" type is not a string in element at index {i}.'
                # Validate that "tag" is a sting
                if not isinstance(elem_dict.get('tag'), str):
                    return False, \
                        '"tagged_elements" data is corrupted. '\
                        f'Field "tag" type is not a string in element at index {i}.'
                if 'heading' not in elem_dict['tag'] and elem_dict['tag'] != 'title':
                    # Validate that non heading elements have a "headings" field
                    if 'headings' not in elem_dict:
                        return False, \
                            '"tagged_elements" data is corrupted. ' \
                            f'Element at index {i} has no attribute "headings"'
                    # Validate that "headings" fields contain the right data
                    for heading in elem_dict.get('headings'):
                        if 'text' not in heading:
                            return False, \
                                '"tagged_elements" data is corrupted. '\
                                f'Heading in element at index {i} has no attribute "text".'
                        # Validate that "tag" is present
                        if 'tag' not in heading:
                            return False, \
                                '"tagged_elements" data is corrupted. '\
                                f'Heading in element at index {i} has no attribute "tag".'
                        # Validate that "text" is a string
                        if not isinstance(heading.get('text'), str):
                            return False, \
                                '"tagged_elements" data is corrupted. '\
                                f'Field "text" type is not a string in heading of element at index {i}.'
                        # Validate that "tag" is a sting
                        if not isinstance(heading.get('tag'), str):
                            return False, \
                                '"tagged_elements" data is corrupted. '\
                                f'Field "tag" type is not a string in heading of element at index {i}.'

        return super().special_validation(payload)
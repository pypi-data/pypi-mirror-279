'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-04-19
Purpose: Maps the input and output fields of services
-----------------------------------------------------
'''
from ..constants import ServiceString


class ServiceIO:
    '''
    Defines the IO of services. The structure is specifically important to determine if
    the input provided by the programmer or other service is acceptable
    '''
    service:ServiceString = None
    required_input_fields = []
    require_one_of_choice = []
    defaults = []
    input_structure = {}
    optional_input_fields = []
    output_structure = {}
    primary_output_field = None

    def __init__(self) -> None:

        self._output_fields = list(self.output_structure.keys())

        if not self.primary_output_field:
            for field in self._output_fields:
                if field != "cost" and field != "charged_character_count":
                    self.primary_output_field = field
                    break
    
    @classmethod
    def special_validation(self, payload):
        return True, None


    @property
    def output_fields(self):
        return self._output_fields

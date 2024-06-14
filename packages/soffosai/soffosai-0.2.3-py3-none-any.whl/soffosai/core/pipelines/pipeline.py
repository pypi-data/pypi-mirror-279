'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-08-14
Purpose: Define the basic pipeline object
-----------------------------------------------------
'''
from typing import List
import soffosai
from soffosai.core.services import SoffosAIService
from ..services import InputConfig

def is_service_input(value):
    if not isinstance(value, dict):
        return False
    return "source" in value and "field" in value


class SoffosPipeline:
    '''
    A controller for consuming multiple Services called stages.
    It validates all inputs of all stages before sending the first Soffos API request to ensure
    that the Pipeline will not waste credits.
    
    ** use_defaults=True means that stages will take input from the previous stages' 
    output of the same field name prioritizing the latest stage's output. 
    If the previous stages does not have it, it will take from the
    pipeline's user_input.  Also, the stages will only be supplied with the required fields + default
    of the require_one_of_choice fields.
    '''
    def __init__(self, services:List[SoffosAIService], use_defaults:bool=False, name=None, **kwargs) -> None:
        self._apikey = kwargs['apikey'] if kwargs.get('apikey') else soffosai.api_key
        self._stages = services
        
        self._input:dict = {}
        self._infos = []
        self._use_defaults = use_defaults
        self._execution_codes = []
        self._termination_codes = []

        error_messages = []
        if not isinstance(services, list):
            error_messages.append('stages field should be a list of SoffosAIService instances')

        service_names = [service.name for service in services]
        for service in services:
            if not isinstance(service, SoffosAIService) and not isinstance(service, SoffosPipeline):
                error_messages.append(f'{service} is not an instance of SoffosAIService or SoffosPipeline.')
            
            if service_names.count(service.name) > 1:
                error_messages.append(f"Service name '{service.name}' is not unique.")

        if len(error_messages) > 0:
            raise ValueError("\\n".join(error_messages))

        # when a pipeline is used as another pipeline's input, it needs a name
        self.name = name

    
    def run(self, user_input):
        original_user_input = user_input.copy()
        if not isinstance(user_input, dict):
            raise ValueError("User input should be a dictionary.")

        if "user" not in user_input:
            raise ReferenceError("'user' is not defined in the user_input.")

        if "text" in user_input:
            user_input['document_text'] = user_input['text']

        if "question" in user_input:
            user_input['message'] = user_input['question']

        if self._use_defaults:
            stages = self.set_defaults(self._stages, user_input)
        else:
            stages = self._stages

        self.validate_pipeline(stages, user_input)

        # termination referencing
        execution_code = user_input.get("execution_code")
        if execution_code:
            execution_code = self._apikey + execution_code
            if execution_code in self._execution_codes:
                raise ValueError("This execution code is still being used in an existing pipeline run.")
            else:
                self._execution_codes.append(execution_code)

        # Initialization of values
        infos = {}
        infos['user_input'] = user_input
        total_cost = 0.00

        # Execute per stage
        for stage in stages:
            # premature termination
            if execution_code in self._termination_codes:
                self._termination_codes.remove(execution_code)
                self._execution_codes.remove(execution_code)
                infos['total_cost'] = total_cost
                infos['warning'] = "This Soffos Pipeline has been prematurely terminated"
                infos['user_input'] = original_user_input
                return infos

            if isinstance(stage, SoffosPipeline):
                stage: SoffosPipeline
                response = stage.run(user_input)
                print(f"Response ready for {stage.name}.")
                pipe_output = {
                    'costs': {}
                }
                for key, value in response.items():
                    if key != 'total_call_cost':
                        for subkey, subvalue in value.items():
                            if subkey == 'cost':
                                pipe_output['costs'][key] = subvalue
                            elif subkey == 'charged_character_count':
                                pipe_output['costs'][key]['charged_character_count'] = subvalue
                            elif subkey == 'unit_price':
                                pipe_output['costs'][key]['unit_price'] = subvalue
                            else:
                                pipe_output[subkey] = subvalue
                    else:
                        total_cost += value
                infos[stage.name] = pipe_output
                continue

            stage: SoffosAIService
            # execute
            print(f"running {stage.name}.")
            tmp_source: dict = stage.source
            payload = {}
            for key, notation in tmp_source.items():
                # prepare payload
                if isinstance(notation, InputConfig):
                    input_dict = {
                        "source": notation.source,
                        "field": notation.field,
                    }
                    if notation.pre_process:
                        input_dict['pre_process'] = notation.pre_process
                    notation = input_dict
                
                if is_service_input(notation): # value is pointing to another Service
                    value = infos[notation['source']][notation['field']]
                    if "pre_process" in notation:
                        if callable(notation['pre_process']):
                            payload[key] = notation['pre_process'](value)
                        else:
                            raise ValueError(f"{stage.name}: pre_process value should be a function.")
                    
                    else:
                        payload[key] = value
                else:
                    payload[key] = notation

            if 'user' not in payload:
                payload["user"] = user_input['user']
            
            payload['apikey'] = self._apikey
            cleaned_payload = stage.clean_payload(payload)
            response = stage.get_response(cleaned_payload)
            if "error" in response:
                infos[stage.name] = response
                infos['total_cost'] = total_cost
                return infos
            
            print(f"Response ready for {stage.name}")
            infos[stage.name] = response
            total_cost += response['cost']['total_cost']

        infos['total_cost'] = total_cost
        infos["user_input"] = original_user_input

        # remove this execution code from execution codes in effect:
        if execution_code:
            self._execution_codes.remove(execution_code)

        return infos


    def validate_pipeline(self, stages, user_input):
        '''
        Before running the first service, the Pipeline will validate all SoffosAIServices if they will all be
        executed successfully with the exception of database and server issues.
        '''
        if not isinstance(user_input, dict):
            raise ValueError("User input should be a dictionary.")

        if "user" not in user_input:
            raise ReferenceError("'user' is not defined in the user_input.")

        if "text" in user_input:
            user_input['document_text'] = user_input['text']

        error_messages = []

        for stage in stages:
            if isinstance(stage, SoffosPipeline):
                stage:SoffosPipeline
                
                if stage._use_defaults:
                    sub_pipe_stages = stage.set_defaults(stage._stages, user_input)
                else:
                    sub_pipe_stages = stage._stages

                stage.validate_pipeline(sub_pipe_stages, user_input)
                continue

            # If stage is a SoffosAIService:
            stage: SoffosAIService
            serviceio = stage._serviceio
            # checking required_input_fields is already handled in the Service's set_input_configs method

            # check if require_one_of_choices is present and not more than one
            if len(serviceio.require_one_of_choice) > 0:
                group_errors = []
                for group in serviceio.require_one_of_choice:
                    found_choices = [choice for choice in group if choice in stage.source]
                    if not found_choices:
                        group_errors.append(f"{stage.name}: Please provide one of these values on your payload: {group}.")
                    elif len(found_choices) > 1:
                        group_errors.append(f"Please include only one of these values: {group}.")
                    
                if len(group_errors) > 0:
                    error_messages.append(". ".join(group_errors))
            
            # check if datatypes are correct:
            for key, notation in stage.source.items():
                required_datatype = serviceio.input_structure.get(key)
                if not required_datatype:
                    continue
                required_datatype = self.get_serviceio_datatype(required_datatype)
                
                # convert InputConfig to dict
                if isinstance(notation, InputConfig): # backwards compatibility
                    input_dict = {
                        "source": notation.source,
                        "field": notation.field,
                    }
                    if notation.pre_process:
                        input_dict['pre_process'] = notation.pre_process
                    notation = input_dict

                if is_service_input(notation):
                    if "pre_process" in notation:
                        continue # will not check for type if there is a helper function
                    
                    if notation['source'] == "user_input":
                        user_input_type = type(user_input[notation['field']])
                        if required_datatype == tuple:
                            allowed_data_types = list(stage._serviceio.input_structure[key])
                            allowed_data_types_str = " or ".join([t.__name__ for t in allowed_data_types])
                            if user_input_type not in allowed_data_types:
                                if notation['field'] == "file":
                                    # TODO: special handling because django, flask, fast api, and regular python has different datatypes for in memory files.
                                    # TODO: should create list of datatypes and put in on file fields of serviceio of all services accepting file
                                    pass
                                else:
                                    error_messages.append(f"{stage.name}:  {user_input_type} required for '{key}' field: but {user_input_type} is provided.")
                        else:
                            if user_input_type != required_datatype:
                                if notation['field'] == "file":
                                    # TODO: special handling because django, flask, fast api, and regular python has different datatypes for in memory files.
                                    pass
                                else:
                                    error_messages.append(f"{stage.name}: {required_datatype} required on user_input '{key}' field but {user_input_type} is provided.")
                    else:
                        source_found = False
                        for subservice in stages:
                            subservice: SoffosAIService
                            if notation['source'] == subservice.name:
                                source_found = True
                                if isinstance(subservice, SoffosPipeline):
                                    break  
                                output_datatype = self.get_serviceio_datatype(subservice._serviceio.output_structure[notation['field']])
                                
                                if type(output_datatype) == tuple:
                                    allowed_data_types = list(stage._serviceio.input_structure[key])
                                    allowed_data_types_str = " or ".join([t.__name__ for t in allowed_data_types])
                                    if user_input_type not in allowed_data_types:
                                        if notation['field'] == "file":
                                            # TODO: special handling because django, flask, fast api, and regular python has different datatypes for in memory files.
                                            # TODO: should create list of datatypes and put in on file fields of serviceio of all services accepting file
                                            pass
                                        else:
                                            error_messages.append(f"{stage.name}:  {user_input_type} required for '{key}' field: but {user_input_type} is provided.")

                                elif output_datatype != required_datatype:
                                    error_messages.append(f"On {stage.name} service: The input datatype required for field ${key} is {required_datatype}. This does not match the datatype to be given by service {subservice.name}'s {notation['field']} field which is {output_datatype}.")
                                break
                        if not source_found:
                            error_messages.append(f"Cannot find service '{notation['source']}'")
                
                else:
                    if required_datatype == tuple:
                        allowed_data_types = list(stage.service._serviceio.input_structure[key])
                        allowed_data_types_str = " or ".join([t.__name__ for t in allowed_data_types])
                        if notation['field'] == "file":
                            # TODO: special handling because django, flask, fast api, and regular python has different datatypes for in memory files.
                            # TODO: should create list of datatypes and put in on file fields of serviceio of all services accepting file
                            pass
                        else:
                            if type(notation) not in allowed_data_types:
                                error_messages.append(f"{stage.name}: {allowed_data_types_str} required for user_input '{key}' field:  but {type(notation).__name__} is provided.")
                    else:
                        if type(notation) != required_datatype and notation!= None:
                            error_messages.append(f"On {stage.name} service: {key} requires ${required_datatype} but ${type(notation)} is provided.")

        if len(error_messages) > 0:
            raise ValueError(error_messages)
        
        return True


    def add_service(self, service):
        if isinstance(service, SoffosAIService) or isinstance(service, SoffosPipeline):
            self._stages.append(service)
        else:
            raise ValueError(f"{service} is not a SoffosAIService instance")

    
    def set_defaults(self, stages, user_input):
        defaulted_stages = []
        for i, stage in enumerate(stages):
            if isinstance(stage, SoffosPipeline):
                continue

            stage: SoffosAIService
            stage_source = {}
            required_keys = stage._serviceio.required_input_fields
            require_one_choices = stage._serviceio.require_one_of_choice
            if len(require_one_choices) > 0:
                for choices in require_one_choices:
                    required_keys.append(choices[0]) # the default argument is the first one
            
            for required_key in required_keys:
                check_key = stage.source.get(required_key)
                if check_key and check_key != "default":
                    stage_source[required_key] = check_key
                    continue

                found_input = False
                for j in range(i-1, -1, -1):
                    stage_for_output:SoffosAIService = stages[j]
                    stage_for_output_output_fields = stage_for_output._serviceio.output_structure
                    if required_key in stage_for_output_output_fields:
                        stage_source[required_key] = {
                            "source": stage_for_output.name,
                            "field": required_key
                        }
                        found_input = True
                
                    # special considerations:
                    elif required_key == "context" and "text" in stage_for_output_output_fields:
                        stage_source["context"] = {
                            "source": stage_for_output.name,
                            "field": "text"
                        }
                        found_input = True

                    elif required_key == "document_text" and "text" in stage_for_output_output_fields:
                        stage_source["document_text"] = {
                            "source": stage_for_output.name,
                            "field": "text"
                        }
                        found_input = True
                    
                if not found_input:
                    if required_key in user_input:
                        stage_source[required_key] = user_input[required_key]
                        stage_source[required_key] = {
                            "source": "user_input",
                            "field": required_key
                        }
                    else:
                        raise ReferenceError(f"Please add {required_key} to user input. The previous Services' outputs do not provide this data.")

            defaulted_stage = stage.set_input_configs(stage.name, stage_source)
            defaulted_stages.append(defaulted_stage)
        
        return defaulted_stages

    
    def terminate(self, termination_code):
        if termination_code:
            self._termination_codes.append(self._apikey + termination_code)
            return {"message": f"Request to terminate job {termination_code} received."}

        return {"message": f"Request to terminate job is not valid (execution code missing)."}


    def get_serviceio_datatype(self, key):
        if isinstance(key, type):
            return key
        return type(key)
    
    def __call__(self, **kwargs):
        return self.run(kwargs)

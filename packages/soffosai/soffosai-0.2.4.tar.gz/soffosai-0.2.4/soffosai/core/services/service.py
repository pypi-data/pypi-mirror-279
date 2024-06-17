'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-04-01
Purpose: The base Service class
-----------------------------------------------------
'''
import inspect
import soffosai
import io
import abc, requests, os, mimetypes, uuid
from soffosai.common.constants import SOFFOS_SERVICE_URL, FORM_DATA_REQUIRED
from soffosai.common.service_io_map import SERVICE_IO_MAP
from soffosai.common.serviceio_fields import ServiceIO


visit_docs_message = "Kindly visit https://platform.soffos.ai/playground/docs#/ for guidance."
input_structure_message = "To learn what the input dictionary should look like, access it by <your_service_instance>.input_structure"


def inspect_arguments(func, *args, **kwargs):
    '''
    Given a function, args and kwargs: 
    create a dictionary with keys as the arg names and values as the arg values
    '''
    # Get the list of argument names
    sig = inspect.signature(func)
    arg_names = list(sig.parameters.keys())

    # Combine positional arguments and keyword arguments
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    combined_args = bound_args.arguments

    # Filter out positional arguments not present in arg_names
    arguments = {name: combined_args[name] for name in arg_names if name in combined_args}
    unziped_kwargs = {}
    for key,value in arguments.items():
        if key != "kwargs":
            if value != None:
                unziped_kwargs[key] = value
        else:
            for key2, value2 in arguments['kwargs'].items():
                if value2 != None:
                    unziped_kwargs[key2] = value2
    
    if unziped_kwargs.get('name'):
        unziped_kwargs.pop('name')

    return unziped_kwargs


def format_uuid(uuid):
    formatted_uuid = '-'.join([
        uuid[:8],
        uuid[8:12],
        uuid[12:16],
        uuid[16:20],
        uuid[20:]
    ])
    return formatted_uuid


def is_valid_uuid(uuid_string):
    if isinstance(uuid_string, type): # coming from pipeline validation, always True because it will come from Soffos Services
        return True

    if "-" not in uuid_string:
        formatted_uuid = format_uuid(uuid_string)
    else:
        formatted_uuid = uuid_string
    try:
        uuid_obj = uuid.UUID(formatted_uuid)
    except ValueError:
        return False
    return str(uuid_obj) == formatted_uuid


class SoffosAIService:
    '''
    Base service class for all Soffos Services
    '''
    def __init__(self, service:str, **kwargs) -> None:            
        if kwargs.get("apikey"):
            apikey = kwargs['apikey']
        else:
            apikey = soffosai.api_key
            
        self.headers = {
            "x-api-key": apikey,
        }
        self._apikey = apikey
        self._service = service
        self._serviceio:ServiceIO = SERVICE_IO_MAP.get(service)
        # In a pipeline, some payload properties are constants and should be related to the Service's instance
        self._payload = {}
        self.name = None # name is required if called in a pipeline


    @property
    def input_structure(self):
        '''
        These are the valid fields of the src dictionary for this service. Take note that some of the fields should not exist at the same time.
        To view fields that cannot co-exist, access the 'choose_one' property.
        '''
        return self._serviceio.input_structure
    

    @property
    def choose_one(self):
        '''
        These keys cannot co-exist in this service's src.
        '''
        return self._serviceio.require_one_of_choice


    def validate_payload(self, payload):
        '''
        checks if the input type is allowed for the service
        '''
        if not isinstance(payload, dict):
            raise TypeError("payload should be a dictionary")

        # check for missing arguments
        user_from_src = payload.get('user')
        if not user_from_src:
            return False, f"{self._service}: user key is required in the payload"

        if len(self._serviceio.required_input_fields) > 0:
            missing_requirements = []
            for required in self._serviceio.required_input_fields:
                if required not in payload:
                    missing_requirements.append(required)
            if len(missing_requirements) > 0:
                return False, f"{self._service}: Please provide {missing_requirements} on your payload. {visit_docs_message}. {input_structure_message}"
        
        if len(self._serviceio.require_one_of_choice) > 0:
            group_error = []
            for group in self._serviceio.require_one_of_choice:
                found_choices = []
                for choice in group:
                    if choice in payload:
                        found_choices.append(choice)
                if len(found_choices) == 0:
                    group_error.append(f"{self._service}: Please provide one of these values on your payload: {group}")
                elif len(found_choices) > 1:
                    group_error.append(f"{self._service}: Please only include one of these values: {group}")
            
            if len(group_error) > 0:
                return False, group_error

        # check if payload has proper type:
        input_structure = self._serviceio.input_structure
        value_errors = []
        for key, value in payload.items():
            if key in input_structure.keys():

                if isinstance(input_structure[key], tuple):
                    allowed_types = input_structure[key]
                    allowed_types_str = "or ".join([t.__name__ for t in allowed_types])
                    if type(value) not in allowed_types:
                        value_errors.append(f"{key} can have {allowed_types_str} but {type(value)} is provided")
                else:
                    if not isinstance(input_structure[key], type):
                        input_type = type(input_structure[key])
                    else:
                        input_type = input_structure[key]

                    if not isinstance(value, input_type) and value != input_type: # the second condition is for pipeline
                        wrong_type = value if isinstance(value, type) else type(value)
                        value_errors.append(f"{key} requires {input_structure[key]} but {wrong_type} is provided.")
        
        special_validation_passed, error_on_special_validation = self._serviceio.special_validation(payload)
        if not special_validation_passed:
            value_errors.append(error_on_special_validation)
        if len(value_errors) > 0:
            return False, value_errors

        if "document_ids" in payload:
            if isinstance(payload['document_ids'], list):
                for _id in payload["document_ids"]:
                    valid_uuid = is_valid_uuid(_id)
                    if not valid_uuid:
                        return False, f"{_id} is invalid document_id"
        
        return True, None


    def get_data(self, payload):
        '''
        Prepare the json or form data input of the service
        '''
        
        request_data = {}
        for key, value in payload.items():
            if key != 'file':
                request_data[key] = value

        return request_data


    def handle_file(self, file_stream, filename, mime_type):
        # Using read(), seek() and other file like object operations on file_stream 
        buffer = file_stream.read()
        file_stream.seek(0)  # it's a good practice to reset the file pointer
        stream = io.BytesIO(buffer)
        file_tuple = (filename, stream, mime_type)
        return file_tuple


    def get_response(self, payload:dict={}) -> dict:
        '''
        Based on the knowledge/context, Soffos AI will now give you the data you need
        '''
        allow_input, message = self.validate_payload(payload)
        if "question" in payload.keys(): # the api receives the question as message.
            payload['message'] = payload['question']

        if not allow_input:
            raise ValueError(message)
        
        if not self._service:
            raise ValueError("Please provide the service you need from Soffos AI.")

        response = None
        data = self.get_data(payload)
        apikey = payload.get("apikey")
        if apikey:
            self.headers["x-api-key"] = apikey
            payload.pop("apikey")

        if self._service not in FORM_DATA_REQUIRED:
            self.headers["content-type"] = "application/json"
            try:
                response = requests.post(
                    url = SOFFOS_SERVICE_URL + self._service + "/",
                    headers = self.headers,
                    json = data,
                    timeout = 120
                )
                response.raise_for_status()
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, 
                    requests.exceptions.Timeout, requests.exceptions.RequestException) as err:
                return_value = {
                    "status": 'Error',
                    "error": str(err)
                }
                try:
                    return_value['detail'] = response.text
                except AttributeError:
                    pass
                return return_value
            
        else:
            file_obj = payload.get('file')
            if isinstance(file_obj, str):
                filename = str(os.path.basename(file_obj))
                mime_type, _ = mimetypes.guess_type(file_obj)
                with open(file_obj, 'rb') as file:
                    files = {
                        "file": (filename, file, mime_type)
                    }
                    try:
                        response = requests.post(
                            url = SOFFOS_SERVICE_URL + self._service + "/",
                            headers = self.headers,
                            data = data,
                            files = files,
                            timeout=120
                        )
                        response.raise_for_status()
                    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, 
                            requests.exceptions.Timeout, requests.exceptions.RequestException) as err:
                        return {
                            "status": 'Error',
                            "error": str(err)
                        }

            else:
                if hasattr(file_obj, "filename"): # handle Flask and Fast API
                    filename = file_obj.filename
                elif hasattr(file_obj, "name"): # django. Flask also have name attribute so we checked filename first
                    filename = file_obj.name
                mime_type, _ = mimetypes.guess_type(filename)
                files = {'file': (filename, file_obj, mime_type)}
                try:
                    response = requests.post(
                        url = SOFFOS_SERVICE_URL + self._service + "/",
                        headers = self.headers,
                        data = data,
                        files = files,
                        timeout=120
                    )
                    response.raise_for_status()
                except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, 
                        requests.exceptions.Timeout, requests.exceptions.RequestException) as err:
                    return {
                        "status": 'Error',
                        "error": str(err)
                    }
        
        if response.ok:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "error": response.text
            }


    def clean_payload(self, raw_payload):
        payload = {}
        if len(raw_payload) == 0:
            raise ValueError("There is no payload")

        for k, v in raw_payload.items():
            if v != None: # if the value is None, we don't pass it to the payload
                payload[k] = v
                if k == "document_name" or k == "chatbot_name":
                    payload["name"] = v
                elif k == "question":
                    payload['message'] = v
        
        return payload


    def __call__(self, **kwargs:dict)->dict:
        payload = self.clean_payload(kwargs)
        return self.get_response(payload=payload)


    @classmethod
    def call(cls, **kwargs):
        instance = cls()
        payload = instance.clean_payload(kwargs)
        return instance.get_response(payload)


    def __str__(self) -> str:
        return self._service


    @abc.abstractmethod
    def provide_output_type(self):
        '''
        Sends back the output datatype of the service
        '''
    

    @abc.abstractmethod
    def provide_source_type(self):
        '''
        Sends back the accepted source datatype of the service
        '''


    @abc.abstractmethod
    def get_default_output_key(self):
        '''
        Sends back the output type of the service
        '''

    def set_input_configs(self, name, **source):
        '''
        Before using a SoffosAIService into a SoffosPipeline, you must setup the service's input configuration.
        '''
        self.name = name
        self.source = source
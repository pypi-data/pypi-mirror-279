'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Audio Converter Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union
from io import BufferedReader

class AudioConverterService(SoffosAIService):
    '''
    Transcribes the given audio. It also detects the language, detects number of
    speakers, and diarizes. "file" or "url" is required, but not both should be
    provided.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.AUDIO_CONVERTER
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, diarize:bool, file:Union[str, BufferedReader]=None, url:str=None, model:str=None) -> dict:
        '''
        Call the Audio Converter Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param diarize: None
        :param file: The audio file to be transcribed.
        :param url: The location of the audio file to be transcribed. Make sure it
            can be accessed publicly. If not, include the athentication
            strings of the url.
        :param model: The model to be used by the audio converter. Can be 'nova 2' or
            'whisper'. Defaults to 'nova 2'.
        :return: number_of_speakers: The number of speakers detected.
        transcripts: The transcription of the audio file or url.
        language: The detected language used by the speakers.
        error: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/audio_converter.py>`_
        '''
        return super().__call__(user=user, diarize=diarize, file=file, url=url, model=model)

    def set_input_configs(self, name:str, diarize:Union[bool, InputConfig], file:Union[str, BufferedReader, InputConfig]=None, url:Union[str, InputConfig]=None, model:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, diarize=diarize, file=file, url=url, model=model)

    @classmethod
    def call(self, user:str, diarize:bool, file:Union[str, BufferedReader]=None, url:str=None, model:str=None) -> dict:
        '''
        Call the Audio Converter Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param diarize: None
        :param file: The audio file to be transcribed.
        :param url: The location of the audio file to be transcribed. Make sure it
            can be accessed publicly. If not, include the athentication
            strings of the url.
        :param model: The model to be used by the audio converter. Can be 'nova 2' or
            'whisper'. Defaults to 'nova 2'.
        :return: number_of_speakers: The number of speakers detected.
        transcripts: The transcription of the audio file or url.
        language: The detected language used by the speakers.
        error: None
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/audio_converter.py>`_
        '''
        return super().call(user=user, diarize=diarize, file=file, url=url, model=model)


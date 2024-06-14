'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Emotion Detection Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class EmotionDetectionService(SoffosAIService):
    '''
    The Emotion Detection module can detect selected emotions within the provided
    text. The original text is chunked to passages of a specified sentence length.
    Smaller chunks yield better accuracy.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.EMOTION_DETECTION
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, text:str, sentence_split:int, sentence_overlap:bool, engine:str=None, emotion_choices:list=['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']) -> dict:
        '''
        Call the Emotion Detection Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to detect emotions from.
        :param sentence_split: The number of sentences of each chunk when splitting the input
            text.
        :param sentence_overlap: Whether to overlap adjacent chunks by 1 sentence. For example,
            with sentence_split=3 and sentence_overlap=true : [[s1, s2, s3],
            [s3, s4, s5], [s5, s6, s7]]
        :param engine: The LLM engine to be used.
        :param emotion_choices: List of emotions to detect in the text. If the field is not
            provided in the payload, or set as null or empty list, it will
            default to all emotion choices. Currently supported emotions are
            listed above in the default emotion values.
        :return: engine: The LLM engine used.
        spans: A list of spans resulting from the specified chunking
            parameters. Each span contains the following fields: text: The
            text of the span. detected_emotions: A list of the emotions
            detected for the specific span. span_start: The starting
            character index of the span in the original input text.
            span_end: The ending character index of the span in the original
            input text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/emotion_detection.py>`_
        '''
        return super().__call__(user=user, text=text, sentence_split=sentence_split, sentence_overlap=sentence_overlap, engine=engine, emotion_choices=emotion_choices)

    def set_input_configs(self, name:str, text:Union[str, InputConfig], sentence_split:Union[int, InputConfig], sentence_overlap:Union[bool, InputConfig], engine:Union[str, InputConfig]=None, emotion_choices:Union[list, InputConfig]=['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']):
        super().set_input_configs(name=name, text=text, sentence_split=sentence_split, sentence_overlap=sentence_overlap, engine=engine, emotion_choices=emotion_choices)

    @classmethod
    def call(self, user:str, text:str, sentence_split:int, sentence_overlap:bool, engine:str=None, emotion_choices:list=['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']) -> dict:
        '''
        Call the Emotion Detection Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param text: Text to detect emotions from.
        :param sentence_split: The number of sentences of each chunk when splitting the input
            text.
        :param sentence_overlap: Whether to overlap adjacent chunks by 1 sentence. For example,
            with sentence_split=3 and sentence_overlap=true : [[s1, s2, s3],
            [s3, s4, s5], [s5, s6, s7]]
        :param engine: The LLM engine to be used.
        :param emotion_choices: List of emotions to detect in the text. If the field is not
            provided in the payload, or set as null or empty list, it will
            default to all emotion choices. Currently supported emotions are
            listed above in the default emotion values.
        :return: engine: The LLM engine used.
        spans: A list of spans resulting from the specified chunking
            parameters. Each span contains the following fields: text: The
            text of the span. detected_emotions: A list of the emotions
            detected for the specific span. span_start: The starting
            character index of the span in the original input text.
            span_end: The ending character index of the span in the original
            input text.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/emotion_detection.py>`_
        '''
        return super().call(user=user, text=text, sentence_split=sentence_split, sentence_overlap=sentence_overlap, engine=engine, emotion_choices=emotion_choices)


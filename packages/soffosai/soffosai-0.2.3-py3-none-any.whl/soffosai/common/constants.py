'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-04-19
Purpose: Organize the constants
-----------------------------------------------------
'''
SOFFOS_SERVICE_URL = "https://api.soffos.ai/service/"

SERVICES_LIST = [
    'answer-scoring',
    'assessment',
    'audio_converter',
    'chat',
    'chatbot/create',
    'chatbot',
    'chatbot/get',
    'chatbot/delete',
    'chatbot/sessions/get',
    'chatbot/sessions/delete',
    'discuss/create',
    'discuss', 
    'discuss/count',
    'discuss/delete',
    'documents/count',
    'documents/ingest', 
    'documents/delete',
    'documents/search',
    'email-analysis', 
    'emotion-detection', 
    'file-converter', 
    'flashcard-generation', 
    'image-analysis',
    'image-generation',
    'intent-classification/confirmation', 
    'intent-classification', 
    'language-detection', 
    'logical-error-detection',
    'microlesson',
    'multiple_choice_qna',
    'natural-sql-generation',
    'natural-sql-generation/table/delete',
    'natural-sql-generation/table/get',
    'natural-sql-generation/table/ingest',
    'ner', 
    'paraphrase', 
    'profanity',
    'qna-generation',
    'question-answering',
    'review-tagger',
    'search-recommendations',
    'sentiment-analysis',
    'simplify',
    'string-similarity',
    'summarization',
    'table-generator',
    'tag',
    'transcript-correction',
    'translation',
    'website-converter',
    'batch-service/'
]

class ServiceString:
    '''
    Contains the list of Soffos services as attributes
    '''
    ANSWER_SCORING = 'answer-scoring'
    ASSESSMENT_GENERATOR = 'assessment'
    AUDIO_CONVERTER = 'audio-converter'
    CHAT = 'chat'
    CHAT_BOT_CREATE = 'chatbot/create'
    CHAT_BOT = 'chatbot'
    CHAT_BOTS_GET = 'chatbot/get'
    CHAT_BOTS_DELETE = 'chatbot/delete'
    CHAT_BOT_GET_USER_SESSIONS = 'chatbot/sessions/get'
    CHAT_BOT_DELETE_USER_SESSIONS = 'chatbot/sessions/delete'
    DISCUSS_CREATE = 'discuss/create'
    DISCUSS_QUERY = 'discuss'
    DISCUSS_RETRIEVE = 'discuss/count'
    DISCUSS_DELETE = 'discuss/delete'
    DISCUSS_COUNT = 'discuss/count'
    DOCUMENTS_COUNT = 'documents/count'
    DOCUMENTS_INGEST = 'documents/ingest'
    DOCUMENTS_DELETE = 'documents/delete'
    DOCUMENTS_SEARCH = 'documents/search'
    EMAIL_ANALYSIS = 'email-analysis'
    EMOTION_DETECTION = 'emotion-detection'
    FILE_CONVERTER = 'file-converter'
    FLASHCARD_GENERATION = 'flashcard-generation'
    IMAGE_ANALYSIS = 'image-analysis'
    IMAGE_GENERATION = 'image-generation'
    INTENT_CLASSIFICATION = 'intent-classification'
    LANGUAGE_DETECTION = 'language-detection'
    LOGICAL_ERROR_DETECTION = 'logical-error-detection'
    MICROLESSON = 'microlesson'
    MULTIPLE_CHOICE_QN_A_GENERATOR = 'multiple_choice_qna'
    NATURAL_S_Q_L_GENERATION = 'natural-sql-generation'
    N_E_R = 'ner'
    PARAPHRASE = 'paraphrase'
    PROFANITY = 'profanity'
    QN_A_GENERATION = 'qna-generation'
    QUESTION_ANSWERING = "question-answering"
    REVIEW_TAGGER = 'review-tagger'
    SEARCH_RECOMMENDATIONS = 'search-recommendations'
    SENTIMENT_ANALYSIS = 'sentiment-analysis'
    SIMPLIFY = 'simplify'
    STRING_SIMILARITY = 'string-similarity'
    SUMMARIZATION = 'summarization'
    TABLE_DELETE = 'natural-sql-generation/table/delete'
    TABLE_GET = 'natural-sql-generation/table/get'
    TABLE_GENERATOR = 'table-generator'
    TABLE_INGEST = 'natural-sql-generation/table/ingest/'
    TAG = 'tag'
    TRANSCRIPT_CORRECTION = 'transcript-correction'
    TRANSLATION = 'translation'
    WEBSITE_CONVERTER = 'website-converter'
    BATCH_SERVICE = 'batch-service2'


FORM_DATA_REQUIRED = [ServiceString.FILE_CONVERTER, ServiceString.AUDIO_CONVERTER]

'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-04-17
Purpose: Soffos Services Objects
-----------------------------------------------------
'''

from .service import SoffosAIService, inspect_arguments
from .input_config import InputConfig

from .answer_scoring import AnswerScoringService
from .assessment_generator import AssessmentGeneratorService
from .audio_converter import AudioConverterService
from .chat import ChatService
from .chat_bot_create import ChatBotCreateService
from .chat_bot import ChatBotService
from .chat_bots_get import ChatBotsGetService
from .chat_bots_delete import ChatBotsDeleteService
from .chat_bot_get_user_sessions import ChatBotGetUserSessionsService
from .chat_bot_delete_user_sessions import ChatBotDeleteUserSessionsService
from .documents_count import DocumentsCountService
from .documents_delete import DocumentsDeleteService
from .documents_ingest import DocumentsIngestService
from .documents_search import DocumentsSearchService
from .email_analysis import EmailAnalysisService
from .emotion_detection import EmotionDetectionService
from .file_converter import FileConverterService
from .image_analysis import ImageAnalysisService
from .image_generation import ImageGenerationService
from .language_detection import LanguageDetectionService
from .discuss_count import DiscussCountService
from .discuss_create import DiscussCreateService
from .discuss_delete import DiscussDeleteService
from .discuss_query import DiscussQueryService
from .logical_error_detection import LogicalErrorDetectionService
from .microlesson import MicrolessonService
from .multiple_choice_qn_a_generator import MultipleChoiceQnAGeneratorService
from .named_entity_recognition import NERService
from .natural_s_q_l_generation import NaturalSQLGenerationService
from .paraphrase import ParaphraseService
from .profanity import ProfanityService
from .qna_generation import QnAGenerationService
from .question_answering import QuestionAnsweringService
from .review_tagger import ReviewTaggerService
from .search_recommendations import SearchRecommendationsService
from .sentiment_analysis import SentimentAnalysisService
from .simplify import SimplifyService
from .string_similarity import StringSimilarityService
from .summarization import SummarizationService
from .table_delete import TableDeleteService
from .table_get import TableGetService
from .table_ingest import TableIngestService
from .table_generator import TableGeneratorService
from .tag import TagService
from .transcript_correction import TranscriptCorrectionService
from .translation import TranslationService
from .website_converter import WebsiteConverterService

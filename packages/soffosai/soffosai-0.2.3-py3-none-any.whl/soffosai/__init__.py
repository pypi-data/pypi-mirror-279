'''
Soffos Inc. Python SDK package
'''

from .client import SoffosAiResponse
from .common.constants import ServiceString
from .core.pipelines import SoffosPipeline, FileIngestPipeline, FileSummaryPipeline, DocumentSummaryPipeline
from .core.services import (
    AnswerScoringService, 
    AudioConverterService,
    ChatBotCreateService,
    ChatBotDeleteUserSessionsService,
    ChatBotGetUserSessionsService,
    ChatBotsDeleteService,
    ChatBotService,
    ChatBotsGetService,
    DiscussQueryService,
    DiscussCountService,
    DiscussCreateService,
    DiscussDeleteService,
    DocumentsIngestService, 
    DocumentsSearchService, 
    DocumentsDeleteService, 
    DocumentsCountService,
    EmailAnalysisService,
    EmotionDetectionService,
    FileConverterService,
    InputConfig,
    LanguageDetectionService,
    LogicalErrorDetectionService,
    MicrolessonService,
    NERService,
    NaturalSQLGenerationService,
    ParaphraseService,
    ProfanityService,
    QnAGenerationService,
    QuestionAnsweringService,
    ReviewTaggerService,
    SearchRecommendationsService,
    SentimentAnalysisService,
    SimplifyService,
    StringSimilarityService,
    SummarizationService,
    TableGeneratorService,
    TagService,
    TableDeleteService,
    TableGetService,
    TableIngestService,
    TranscriptCorrectionService,
    TranslationService,
    WebsiteConverterService
)
from .common.constants import ServiceString
from .core import services as SoffosAIServices
from .core import pipelines as SoffosAIPipelines
import os

api_key = os.environ.get("SOFFOSAI_API_KEY")

__all__ = [
    "api_key",
    "ServiceString",
    "SoffosAiResponse",
    "SoffosAIServices",
    "SoffosAIPipelines",

    "AnswerScoringService",
    "AudioConverterService",
    "ChatBotCreateService",
    "ChatBotDeleteUserSessionsService",
    "ChatBotGetUserSessionsService",
    "ChatBotsDeleteService",
    "ChatBotService",
    "ChatBotsGetService",
    "DiscussQueryService",
    "DiscussCountService",
    "DiscussCreateService",
    "DiscussDeleteService",
    "DocumentsCountService",
    "DocumentsIngestService", 
    "DocumentsSearchService", 
    "DocumentsDeleteService", 
    "EmailAnalysisService",
    "EmotionDetectionService",
    "FileConverterService",
    "LanguageDetectionService",
    "LogicalErrorDetectionService",
    "MicrolessonService",
    "NERService",
    "NaturalSQLGenerationService",
    "ParaphraseService",
    "ProfanityService",
    "QnAGenerationService",
    "QuestionAnsweringService",
    "ReviewTaggerService",
    "SearchRecommendationsService",
    "SentimentAnalysisService",
    "SimplifyService",
    "StringSimilarityService",
    "SummarizationService",
    "TableGeneratorService",
    "TagService",
    "TableDeleteService",
    "TableGetService",
    "TableIngestService",
    "TranscriptCorrectionService",
    "TranslationService",
    "WebsiteConverterService",

    "SoffosPipeline", 
    "FileIngestPipeline", 
    "FileSummaryPipeline", 
    "DocumentSummaryPipeline",

    "InputConfig"
]

__title__ = "soffosai"
__description__ = "Python SDK for Soffos.ai API"
__version__ = "0.1.8"

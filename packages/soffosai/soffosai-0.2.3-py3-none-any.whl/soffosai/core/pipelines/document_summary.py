'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-06-30
Purpose: Define the standard Pipeline for converting, summarizing an ingested document
-----------------------------------------------------
'''
from soffosai.core.services import DocumentsSearchService, SummarizationService, InputConfig
from soffosai.core.pipelines import SoffosPipeline


def get_text_from_passages(passages):
    text = ""
    for passage in passages:
        text = text + passage['content']
    return text


class DocumentSummaryPipeline(SoffosPipeline):
    '''
    A Soffos Pipeline that takes document_ids, then summarizes the content.
    The output is a list containing the output object of file converter and summarization.
    '''
    def __init__(self, **kwargs) -> None:
        document_search = DocumentsSearchService().set_input_configs(
            name = "doc_search",
            document_ids= {"source": "user_input", "field": "document_ids"}
        )
        
        summarization = SummarizationService().set_input_configs(
            name = "summarization",
            text = InputConfig("doc_search", "passages", get_text_from_passages),
            sent_length = InputConfig("user_input", "sent_length")
        )

        services = [document_search, summarization]
        use_defaults = False
        super().__init__(services=services, use_defaults=use_defaults, **kwargs)


    def __call__(self, user, document_ids, sent_length):
        return super().__call__(user=user, document_ids=document_ids, sent_length=sent_length)

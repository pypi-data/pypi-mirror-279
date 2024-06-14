'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-06-30
Purpose: Define the standard Pipeline for converting and summarizing a file
-----------------------------------------------------
'''
from soffosai.core.services import FileConverterService, SummarizationService, InputConfig
from soffosai.core.pipelines import SoffosPipeline

class FileSummaryPipeline(SoffosPipeline):
    '''
    A Soffos Pipeline that takes a file, convert it to its text content then summarizes it.
    The output is a list containing the output object of file converter and summarization.
    '''
    def __init__(self, **kwargs) -> None:

        file_converter = FileConverterService().set_input_configs(
            name = "fileconverter",
            file = InputConfig("user_input", "file")
        )
        summarization = SummarizationService().set_input_configs(
            name = "summary",
            text = InputConfig("fileconverter", "text"),
            sent_length = InputConfig("user_input", "sent_length")
        )

        services = [file_converter, summarization]
        use_defaults = False
        super().__init__(services=services, use_defaults=use_defaults, **kwargs)


    def __call__(self, user, file, sent_length):
        return super().__call__(user=user, file=file, sent_length=sent_length)

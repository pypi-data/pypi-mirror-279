'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-06-29
Purpose: Define the standard Pipeline for converting then ingesting a file
-----------------------------------------------------
'''
from soffosai.core.services import FileConverterService, DocumentsIngestService, InputConfig
from soffosai.core.pipelines import SoffosPipeline

class FileIngestPipeline(SoffosPipeline):
    '''
    A Soffos Pipeline that takes a file, convert it to its text content then saves it to Soffos db.
    the output is a list containing the output object of file converter and document ingest
    '''
    def __init__(self, **kwargs) -> None:


        file_converter = FileConverterService().set_input_configs(
            name = "fileconverter",
            file = InputConfig("user_input", "file")
        )
        document_ingest = DocumentsIngestService().set_input_configs(
            name = "ingest",
            document_name = InputConfig("user_input", "file"),
            text = InputConfig("fileconverter", "text")
        )

        services = [file_converter, document_ingest]
        use_defaults = False
        super().__init__(services=services, use_defaults=use_defaults, **kwargs)


    def __call__(self, user, file):
        return super().__call__(user=user, file=file)

'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use File Converter Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union
from io import BufferedReader

class FileConverterService(SoffosAIService):
    '''
    The File Converter extracts text from various types of files. It tags elements
    within structured DOCX documents and provides a list of labelled text spans.
    Additionally, the normalize feature is available which uses a machine learning
    approach to organize messy outputs as well as tag and label document elements
    based on the whitespace formatting (new lines, spaces, etc.) and the content
    itself. The normalize feature is more suited for unstructured documents such as
    plain text or PDFs (scanned and searchable) that are almost impossible to
    process reliably with a single rule-based approach due to their inconsistent
    and often complicated formatting. Note: Character volume is not charged when
    calling this module unless the normalize feature is enabled. When enabled,
    characters in the normalized_text output field are charged. Otherwise, only the
    base API call cost is charged. Tip: DOCX documents are well structured and can
    be processed reliably without enabling normalize. DOCX is the only type of
    document that produces tagged_elements. Use the normalize feature only with
    DOCX documents that do not have a good heading/list structure such as DOCX that
    have been converted from PDF.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.FILE_CONVERTER
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, file:BufferedReader, normalize:str, engine:str=None) -> dict:
        '''
        Call the File Converter Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param file: None
        :param normalize: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        normalize: None
        text: Raw text extracted from the document.
        tagged_elements: A list of dictionaries of all the extracted text snippets and
            their tags. Each dictionary has the following fields: text: The
            text of the snippet. tag: A tag. Detectable elements: paragraph,
            heading, bullet_list, table_of_contents. headings: A list of
            dictionaries representing the headings which this element is
            under. Each dictionary contains the text and tag fields of each
            heading. This is useful for sorting and labelling the content.
            Other element-specific fields: bullets: Available only
            bullet_list elements. Contains all bullets and their sub-bullets
            in a nested structure. contents: Available only in
            table_of_content elements. Contains the headings andn
            sub-headings of the document's table of contents. heading:
            Available only in table_of_content elements. It is the heading
            of the document's table of contents.
        normalized_text: Resulting text after normalization.
        normalized_tagged_elements: Similar to the standard tagged_elements. Detectable elements:
            paragraph, heading, bullet_list, quote.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/file_converter.py>`_
        '''
        return super().__call__(user=user, file=file, normalize=normalize, engine=engine)

    def set_input_configs(self, name:str, file:Union[str, BufferedReader, InputConfig], normalize:Union[str, InputConfig], engine:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, file=file, normalize=normalize, engine=engine)

    @classmethod
    def call(self, user:str, file:BufferedReader, normalize:str, engine:str=None) -> dict:
        '''
        Call the File Converter Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param file: None
        :param normalize: None
        :param engine: The LLM engine to be used.
        :return: engine: The LLM engine used.
        normalize: None
        text: Raw text extracted from the document.
        tagged_elements: A list of dictionaries of all the extracted text snippets and
            their tags. Each dictionary has the following fields: text: The
            text of the snippet. tag: A tag. Detectable elements: paragraph,
            heading, bullet_list, table_of_contents. headings: A list of
            dictionaries representing the headings which this element is
            under. Each dictionary contains the text and tag fields of each
            heading. This is useful for sorting and labelling the content.
            Other element-specific fields: bullets: Available only
            bullet_list elements. Contains all bullets and their sub-bullets
            in a nested structure. contents: Available only in
            table_of_content elements. Contains the headings andn
            sub-headings of the document's table of contents. heading:
            Available only in table_of_content elements. It is the heading
            of the document's table of contents.
        normalized_text: Resulting text after normalization.
        normalized_tagged_elements: Similar to the standard tagged_elements. Detectable elements:
            paragraph, heading, bullet_list, quote.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/file_converter.py>`_
        '''
        return super().call(user=user, file=file, normalize=normalize, engine=engine)


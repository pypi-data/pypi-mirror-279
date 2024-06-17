'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2024-03-03
Purpose: Easily use Question Answering Service
-----------------------------------------------------
'''
from .service import SoffosAIService
from .input_config import InputConfig
from soffosai.common.constants import ServiceString
from typing import Union


class QuestionAnsweringService(SoffosAIService):
    '''
    This module is a combination of various sub-modules that enable users to get
    accurate answers on questions posed on a large amount of content. It includes
    basic intent recognition capabilities to enable appropriate responses to
    incorrect or profane language, or typical personal questions like "How are
    you?" and greetings.
    '''

    def __init__(self, **kwargs) -> None:
        service = ServiceString.QUESTION_ANSWERING
        super().__init__(service, **kwargs)
    
    def __call__(self, user:str, question:str, engine:str=None, document_text:str=None, document_ids:list=None, check_ambiguity:bool=True, check_query_type:bool=True, generic_response:bool=None, meta:dict=None, message_id:str=None) -> dict:
        '''
        Call the Question Answering Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param question: A natural language query/question.
        :param engine: The LLM engine to be used.
        :param document_text: The text to be used as the context to formulate the answer.
        :param document_ids: A list of unique IDs referencing pre-ingested documents to be
            used as the context to formulate the answer.
        :param check_ambiguity: When true, it checks whether the message contains a pronoun
            which is impossible to resolve and responds appropriately to
            avoid low quality or inaccurate answers. This is most useful
            when this module is used for conversational agents. For example:
            "What was his most famous invention?" Queries with pronouns that
            also contain the entity that the pronoun refers to are not
            rejected. For example: "What was Tesla's most famous invention
            and when did he create it?" In this case, the AI can infer that
            he refers to Tesla. Set this to false only when getting the most
            relevant content as the answer has equal or higher importance
            than the question being rejected or the answer being
            ambiguous/inaccurate.
        :param check_query_type: When true, it will check whether the message is a natural
            language question, or whether it is a keyword query or a
            statement and respond appropriately if the message is not a
            question. The module is capable of returning a relevant answer
            to keyword or poorly formulated queries, but this option can
            help restrict the input. Set to false only when you wish the
            module to attempt to answer the query regardless of its type or
            syntactical quality.
        :param generic_response: In addition to checking for ambiguity or query type, this module
            performs other checks such as profanity, language, etc.. If the
            input query fails in one of these checks, it will reject the
            query by responding with a message that points out the issue.
            When true, the module will respond with a generic message
            without giving the reason as to why the message was rejected,
            which is the same behavior as when it cannot find an answer to
            the query in the provided context.
        :param meta: A dictionary of key-value pairs for filtering the context to
            documents with matching meta fields. Refer to the document
            ingestion API for more details.
        :param message_id: A unique ID representing the message and its associated response.
        :return: engine: The LLM engine used.
        message_id: A unique ID representing the message and its associated response.
        answer: The answer to the query. In cases where the query failed a
            check, and depending on the above explained parameters, this
            will be a message that indicates that an answer could not be
            retrieved.
        context: The merged passages text.
        valid_query: Boolean flag denoting whether the query failed a check.
        no_answer: Boolean flag denoting that the query has passed the checks, but
            no answer for it was found in the context.
        highlights: A list of dictionaries representing sentences within the context
            which are highly similar to the answer. Each dictionary has the
            following fields: span: A list with the start and end character
            index of the sentence within context. sentence: The sentence
            text.
        passages: A list of dictionaries representing the most relevant passages
            of the queried documents. The first step for generating an
            answer is finding the most relevant passages from a big
            knowledge base. The passages are matched with a combination of
            keyword and semantic similarity. Each passage has the following
            fields: text document_name document_id scores: A dictionary
            containing the matching scores for either or both keyword,
            semantic.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/question_answering.py>`_
        '''
        return super().__call__(user=user, question=question, engine=engine, document_text=document_text, document_ids=document_ids, check_ambiguity=check_ambiguity, check_query_type=check_query_type, generic_response=generic_response, meta=meta, message_id=message_id)

    def set_input_configs(self, name:str, question:Union[str, InputConfig], engine:Union[str, InputConfig]=None, document_text:Union[str, InputConfig]=None, document_ids:Union[list, InputConfig]=None, check_ambiguity:Union[bool, InputConfig]=True, check_query_type:Union[bool, InputConfig]=True, generic_response:Union[bool, InputConfig]=None, meta:Union[dict, InputConfig]=None, message_id:Union[str, InputConfig]=None):
        super().set_input_configs(name=name, question=question, engine=engine, document_text=document_text, document_ids=document_ids, check_ambiguity=check_ambiguity, check_query_type=check_query_type, generic_response=generic_response, meta=meta, message_id=message_id)

    @classmethod
    def call(self, user:str, question:str, engine:str=None, document_text:str=None, document_ids:list=None, check_ambiguity:bool=True, check_query_type:bool=True, generic_response:bool=None, meta:dict=None, message_id:str=None) -> dict:
        '''
        Call the Question Answering Service
        
        :param user: The ID of the user accessing the Soffos API.
            This string will be used for throttling and profanity tracking.
            Soffos assumes that the owner of the api is an application (app) and that app has users.
            Soffos API will accept any string."
        :param question: A natural language query/question.
        :param engine: The LLM engine to be used.
        :param document_text: The text to be used as the context to formulate the answer.
        :param document_ids: A list of unique IDs referencing pre-ingested documents to be
            used as the context to formulate the answer.
        :param check_ambiguity: When true, it checks whether the message contains a pronoun
            which is impossible to resolve and responds appropriately to
            avoid low quality or inaccurate answers. This is most useful
            when this module is used for conversational agents. For example:
            "What was his most famous invention?" Queries with pronouns that
            also contain the entity that the pronoun refers to are not
            rejected. For example: "What was Tesla's most famous invention
            and when did he create it?" In this case, the AI can infer that
            he refers to Tesla. Set this to false only when getting the most
            relevant content as the answer has equal or higher importance
            than the question being rejected or the answer being
            ambiguous/inaccurate.
        :param check_query_type: When true, it will check whether the message is a natural
            language question, or whether it is a keyword query or a
            statement and respond appropriately if the message is not a
            question. The module is capable of returning a relevant answer
            to keyword or poorly formulated queries, but this option can
            help restrict the input. Set to false only when you wish the
            module to attempt to answer the query regardless of its type or
            syntactical quality.
        :param generic_response: In addition to checking for ambiguity or query type, this module
            performs other checks such as profanity, language, etc.. If the
            input query fails in one of these checks, it will reject the
            query by responding with a message that points out the issue.
            When true, the module will respond with a generic message
            without giving the reason as to why the message was rejected,
            which is the same behavior as when it cannot find an answer to
            the query in the provided context.
        :param meta: A dictionary of key-value pairs for filtering the context to
            documents with matching meta fields. Refer to the document
            ingestion API for more details.
        :param message_id: A unique ID representing the message and its associated response.
        :return: engine: The LLM engine used.
        message_id: A unique ID representing the message and its associated response.
        answer: The answer to the query. In cases where the query failed a
            check, and depending on the above explained parameters, this
            will be a message that indicates that an answer could not be
            retrieved.
        context: The merged passages text.
        valid_query: Boolean flag denoting whether the query failed a check.
        no_answer: Boolean flag denoting that the query has passed the checks, but
            no answer for it was found in the context.
        highlights: A list of dictionaries representing sentences within the context
            which are highly similar to the answer. Each dictionary has the
            following fields: span: A list with the start and end character
            index of the sentence within context. sentence: The sentence
            text.
        passages: A list of dictionaries representing the most relevant passages
            of the queried documents. The first step for generating an
            answer is finding the most relevant passages from a big
            knowledge base. The passages are matched with a combination of
            keyword and semantic similarity. Each passage has the following
            fields: text document_name document_id scores: A dictionary
            containing the matching scores for either or both keyword,
            semantic.
        :Examples
        Detailed examples can be found at `Soffos Github Repository <https://github.com/Soffos-Inc/soffosai-python/tree/master/samples/services/question_answering.py>`_
        '''
        return super().call(user=user, question=question, engine=engine, document_text=document_text, document_ids=document_ids, check_ambiguity=check_ambiguity, check_query_type=check_query_type, generic_response=generic_response, meta=meta, message_id=message_id)


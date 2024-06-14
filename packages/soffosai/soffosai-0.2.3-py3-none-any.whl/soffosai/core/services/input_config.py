'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-10-05
Purpose: Input Configuration used in configuring an input source of a Node.
'''

class InputConfig:
    '''
    Input Configuration for Pipeline Nodes.
    When sequencing Nodes within a Pipeline this helps configure which Node's output is used as
    which Node's input.
    '''

    def __init__(self, source:str, field:str, pre_process:callable=None):
        """
        :param source: The name of the SoffosAIService or SoffosPipeline from \
            where the input of the current SoffosAIService should be taken from.\
            It can also be "user_input" if the input will come from the user and \
            not from a Service/SoffosPipeline.
        :param field: The name of the output field of the "source".
        :param pre_process (optional): A function to preprocess the data from source[field].
        """
        self.source = source
        self.field = field
        self.pre_process = pre_process
        if pre_process:
            if not callable(pre_process):
                raise TypeError("pre_process should be callable.")

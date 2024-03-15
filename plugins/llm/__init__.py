from typing import Dict, Any, Union
from langchain.pydantic_v1 import create_model
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .._interface import LLMFmt, LCEL
from .._utils import create_pydantic_dict, prompt_template
# Import the model
from .gpt import model as openai_model
from .gemini import model as gemini_model


class LLMGenerator:
    '''
    Large Language Model (LLM) wrapper module.
    '''

    def __init__(self, fmt: LLMFmt = {}):
        self.fmt = fmt
        self.model = openai_model
        self.parser = self.__parser(fmt=self.fmt)
        self.template = self.__template()

    def __parser(self, fmt: LLMFmt):
        '''
        Parses for the model's format output.
        '''
        PydanticObject = create_model(
            "LLMParser", **create_pydantic_dict(fmt)
        )
        return JsonOutputParser(pydantic_object=PydanticObject)

    def __template(self):
        '''
        Get the template for the model.
        '''
        return PromptTemplate(
            template=prompt_template,
            input_variables=["system", "prompt"],
            partial_variables={
                "instruction": self.parser.get_format_instructions()},
        )

    def set_parser(self, fmt: LLMFmt) -> None:
        '''
        Set the parser object.
        '''
        self.fmt = fmt
        self.parser = self.__parser(fmt=fmt)
        self.template = self.__template()

    def generate(self, system: str, prompt: str) -> Union[Dict[str, Any], Any]:
        chain: LCEL = self.template | self.model | self.parser

        return chain.invoke({"system": system, "prompt": prompt})
